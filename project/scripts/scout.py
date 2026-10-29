"""Poll the watchlist's job feeds and keep only new, relevant, recent roles.

No AI tokens: everything here is plain filtering. Output goes to out/jobs/<date>.json and
.csv, sorted by a keyword-fit score; only the top of that list is worth an AI read.

Filters come from data/profile.json "search": regions (codes in REGIONS), include_title_words,
exclude_title_words, strong_title_words, years. Defaults suit software engineers; any field works.

Usage: py -3 scout.py [--days 7] [--no-mark] [--only "Stripe,Shopify"]
"""
import argparse
import csv
import datetime as dt
import html
import json
import os
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

from discover_ats import fetch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Defaults fit an early-career software engineer. profile.json "search" replaces each list for any
# other field: include_title_words (a title must match one), exclude_title_words (skip if any match),
# strong_title_words (+10 score). A sales candidate: include ["sales", "account executive", ...].
INCLUDE_TITLE = ["engineer", "engineering", "developer", "sde", "swe", "programmer"]
STRONG_TITLE = ["backend", "back-end", r"full[- ]?stack", "software engineer", "sde", "ai engineer",
                "applied ai", "platform", "product engineer"]
EXCLUDE_TITLE = ["senior", "sr", "staff", "principal", "lead", "manager", "director", "head", "vp",
                 "vice president", "architect", "intern", "internship", "sales", r"solutions?", "support",
                 "customer", r"recruit\w*", "analyst", "hardware", "mechanical", "electrical", "civil",
                 "firmware", "embedded", "verification", "asic", "fpga", "qa", "test", "iii", "iv",
                 "l5", "l6", "e5", "e6"]

REGIONS = [
    ("IN", r"india|bengaluru|bangalore|pune|hyderabad|mumbai|gurgaon|gurugram|noida|delhi|chennai|kolkata|ahmedabad"),
    ("UK", r"united kingdom|\buk\b|london|manchester|edinburgh|cambridge, uk|england"),
    ("DE", r"germany|berlin|munich|münchen|hamburg|frankfurt|cologne|köln"),
    ("NL", r"netherlands|amsterdam|rotterdam|utrecht|eindhoven|the hague"),
    ("AU", r"australia|sydney|melbourne|brisbane|perth"),
    ("CA", r"canada|toronto|vancouver|montreal|ottawa|calgary|waterloo"),
    ("IE", r"ireland|dublin|cork|galway"),
    ("SG", r"singapore"),
    ("AE", r"united arab emirates|\buae\b|dubai|abu dhabi"),
    ("US", r"united states|\busa?\b|u\.s\.|new york|san francisco|seattle|bay area|mountain view|"
           r"palo alto|austin|boston|chicago|los angeles|sunnyvale|san jose|menlo park|denver"),
    ("Remote", r"remote|anywhere|distributed"),
]
NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                "eight": 8, "nine": 9, "ten": 10}
YEARS = re.compile(r"\b(\d{1,2}|" + "|".join(NUMBER_WORDS) + r")\s*\+?\s*(?:(?:-|–|to)\s*\d{1,2}\s*)?\+?\s*"
                   r"(?:years?|yrs?)\b(?=[^.]{0,60}\bexperience)", re.I)


def _any(words, text):
    return bool(words) and bool(re.search(r"\b(" + "|".join(words) + r")\b", text, re.I))


def title_ok(title, exclude=None, include=None):
    return (_any(INCLUDE_TITLE if include is None else include, title)
            and not _any(EXCLUDE_TITLE if exclude is None else exclude, title))


def region_of(location):
    loc = (location or "").lower()
    for code, pattern in REGIONS:
        if re.search(pattern, loc):
            return code
    return None


def min_years(text):
    found = [int(NUMBER_WORDS.get(m.group(1).lower(), m.group(1))) for m in YEARS.finditer(text or "")]
    return max(found) if found else None


def parse_posted(value, today):
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        secs = value / 1000 if value > 1e11 else value
        return dt.datetime.fromtimestamp(secs, dt.timezone.utc).date()
    v = value.strip()
    low = v.lower()
    if "today" in low:
        return today
    if "yesterday" in low:
        return today - dt.timedelta(days=1)
    m = re.search(r"(\d+)\+?\s*days? ago", low)
    if m:
        return today - dt.timedelta(days=int(m.group(1)))
    try:
        return dt.date.fromisoformat(v[:10])
    except ValueError:
        pass
    try:
        return dt.datetime.strptime(v, "%B %d, %Y").date()
    except ValueError:
        return None


def plain(text):
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def _skill_terms(profile):
    for items in profile["skills"].values():
        for skill in items:
            yield skill, [skill] + profile.get("keyword_aliases", {}).get(skill, [])


def keyword_hits(text, profile):
    hits = []
    for skill, terms in _skill_terms(profile):
        for term in terms:
            flags = 0 if len(term) <= 3 else re.I  # "Go", "RAG", "S3" only count in their own casing
            if re.search(r"(?<![\w.+#-])" + re.escape(term) + r"(?![\w+#])", text, flags):
                hits.append(skill)
                break
    return hits


def score(job, profile, today):
    text = f"{job['title']} {job.get('description', '')}"
    s = min(len(keyword_hits(text, profile)), 8) / 8 * 60
    s += 10 if _any(profile.get("search", {}).get("strong_title_words", STRONG_TITLE), job["title"]) else 0
    posted = job.get("posted")
    if posted is None:
        s += 5
    else:
        age = (today - posted).days
        s += 20 if age <= 1 else 15 if age <= 3 else 8 if age <= 7 else 3 if age <= 14 else 0
    years = min_years(job.get("description", ""))
    gap = 0 if years is None else years - profile.get("search", {}).get("years", 2)
    s += 10 if gap <= 0 else 0 if gap == 1 else -15 if gap == 2 else -30
    return max(0, min(100, round(s)))


def _job(ats, board, jid, title, url, location, posted_raw, description):
    return {"id": f"{ats}:{board}:{jid}", "ats": ats, "title": title.strip(), "url": url,
            "location": location or "", "posted_raw": posted_raw, "description": description}


def from_greenhouse(board, j):
    return _job("greenhouse", board, j["id"], j["title"], j["absolute_url"], (j.get("location") or {}).get("name"),
                j.get("first_published") or j.get("updated_at"), plain(j.get("content")))


def from_lever(board, j):
    parts = [j.get("descriptionPlain", "")] + [f"{l.get('text', '')}: {plain(l.get('content'))}" for l in j.get("lists", [])]
    parts.append(j.get("additionalPlain", ""))
    return _job("lever", board, j["id"], j["text"], j["hostedUrl"], (j.get("categories") or {}).get("location"),
                j.get("createdAt"), " ".join(p for p in parts if p))


def from_ashby(board, j):
    locs = [j.get("location") or ""] + [s.get("location", "") for s in j.get("secondaryLocations") or []]
    return _job("ashby", board, j["id"], j["title"], j["jobUrl"], "; ".join(l for l in locs if l),
                j.get("publishedAt"), j.get("descriptionPlain") or plain(j.get("descriptionHtml")))


def from_smartrecruiters(board, j):
    loc = j.get("location") or {}
    where = ", ".join(x for x in (loc.get("city"), loc.get("country")) if x) + (" (remote)" if loc.get("remote") else "")
    return _job("smartrecruiters", board, j["id"], j["name"], f"https://jobs.smartrecruiters.com/{board}/{j['id']}",
                where, j.get("releasedDate"), "")


def unseen(jobs, seen):
    return [j for j in jobs if j["id"] not in seen]


# ---- network fetchers (thin; everything testable lives above) ----

def fetch_board(company, query="software engineer"):
    ats, board = company["ats"], company["board"]
    if ats == "greenhouse":
        d = json.loads(fetch(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true", timeout=60))
        return [from_greenhouse(board, j) for j in d["jobs"]]
    if ats == "lever":
        return [from_lever(board, j) for j in json.loads(fetch(f"https://api.lever.co/v0/postings/{board}?mode=json", timeout=60))]
    if ats == "ashby":
        d = json.loads(fetch(f"https://api.ashbyhq.com/posting-api/job-board/{board}", timeout=60))
        return [from_ashby(board, j) for j in d["jobs"]]
    if ats == "smartrecruiters":
        d = json.loads(fetch(f"https://api.smartrecruiters.com/v1/companies/{board}/postings?limit=100"))
        return [from_smartrecruiters(board, j) for j in d.get("content", [])]
    if ats == "workday":
        return fetch_workday(*board.split("|"), query)
    if ats == "amazon":
        return fetch_amazon(query)
    return []


def fetch_workday(host, tenant, site, query):
    jobs = []
    for offset in range(0, 100, 20):
        d = json.loads(fetch(f"https://{host}/wday/cxs/{tenant}/{site}/jobs",
                             {"appliedFacets": {}, "limit": 20, "offset": offset, "searchText": query}))
        for p in d.get("jobPostings", []):
            path = p.get("externalPath", "")
            j = _job("workday", tenant, path.rsplit("_", 1)[-1], p.get("title", ""), f"https://{host}/en-US/{site}{path}",
                     p.get("locationsText"), p.get("postedOn"), "")
            j["_detail"] = f"https://{host}/wday/cxs/{tenant}/{site}{path}"
            jobs.append(j)
        if len(d.get("jobPostings", [])) < 20:
            break
    return jobs


def fetch_amazon(query):
    jobs = []
    for country in ("IND", "DEU", "NLD", "GBR", "AUS", "USA"):
        q = urllib.parse.urlencode({"base_query": query, "normalized_country_code[]": country,
                                    "result_limit": 100, "sort": "recent"})
        for j in json.loads(fetch(f"https://www.amazon.jobs/en/search.json?{q}", timeout=60)).get("jobs", []):
            jobs.append(_job("amazon", "amazon", j.get("id_icims") or j.get("id"), j.get("title", ""),
                             "https://www.amazon.jobs" + j.get("job_path", ""), j.get("normalized_location") or j.get("location"),
                             j.get("posted_date"), plain(f"{j.get('description', '')} {j.get('basic_qualifications', '')} "
                                                         f"{j.get('preferred_qualifications', '')}")))
    return jobs


def add_workday_detail(job):
    try:
        info = json.loads(fetch(job.pop("_detail"))).get("jobPostingInfo", {})
        job["description"] = plain(info.get("jobDescription"))
    except Exception:
        pass
    return job


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7, help="keep jobs posted within this many days (unknown dates kept)")
    ap.add_argument("--no-mark", action="store_true", help="don't record results as seen")
    ap.add_argument("--only", help="comma-separated company names")
    a = ap.parse_args()
    today = dt.date.today()
    profile = json.load(open(os.path.join(ROOT, "data", "profile.json"), encoding="utf-8"))
    search = profile.get("search", {})
    regions = set(search.get("regions") or [code for code, _ in REGIONS])
    query = (search.get("keywords") or ["software engineer"])[0]  # Workday / Amazon need a search term
    companies = json.load(open(os.path.join(ROOT, "data", "companies.json"), encoding="utf-8"))
    if a.only:
        names = {n.strip().lower() for n in a.only.split(",")}
        companies = [c for c in companies if c["name"].lower() in names]
    seen_path = os.path.join(ROOT, "data", "seen.json")
    seen = set(json.load(open(seen_path))) if os.path.exists(seen_path) else set()

    feeds = [c for c in companies if c["ats"] != "chrome"]

    def pull(c):
        try:
            return c, fetch_board(c, query), None
        except Exception as e:  # one broken board must not stop the run
            return c, [], str(e)

    kept, errors, total = [], [], 0
    with ThreadPoolExecutor(12) as pool:
        for c, jobs, err in pool.map(pull, feeds):
            if err:
                errors.append(f"{c['name']}: {err}")
            total += len(jobs)
            for j in jobs:
                j["company"], j["segment"] = c["name"], c["segment"]
                j["region"] = region_of(j["location"])
                j["posted"] = parse_posted(j["posted_raw"], today)
                fresh = j["posted"] is None or (today - j["posted"]).days <= a.days
                if title_ok(j["title"], search.get("exclude_title_words"), search.get("include_title_words")) and j["region"] in regions and fresh:
                    kept.append(j)
    kept = unseen(kept, seen)
    with ThreadPoolExecutor(12) as pool:
        kept = list(pool.map(lambda j: add_workday_detail(j) if "_detail" in j else j, kept))
    for j in kept:
        j["years"] = min_years(j["description"])
        j["hits"] = keyword_hits(f"{j['title']} {j['description']}", profile)
        j["score"] = score(j, profile, today)
    kept.sort(key=lambda j: (j["score"], j["posted"] or dt.date.min), reverse=True)  # best fit, then newest

    out_dir = os.path.join(ROOT, "out", "jobs")
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.join(out_dir, today.isoformat())
    rows = [{k: (v.isoformat() if isinstance(v, dt.date) else v) for k, v in j.items() if k != "description"} for j in kept]
    json.dump([dict(r, description=j["description"]) for r, j in zip(rows, kept)],
              open(stem + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cols = ["score", "company", "title", "region", "location", "posted", "years", "segment", "url", "id"]
    with open(stem + ".csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    if not a.no_mark:
        json.dump(sorted(seen | {j["id"] for j in kept}), open(seen_path, "w"))

    print(f"{len(feeds)} feeds, {total} postings scanned, {len(kept)} new matches -> {stem}.csv")
    for r in rows[:25]:
        print(f"{r['score']:>3}  {r['posted'] or '?':10}  {r['region']:6}  {r['company'][:18]:18}  {r['title'][:60]}")
    for e in errors:
        print("error:", e)
    manual = [c["name"] for c in companies if c["ats"] == "chrome"]
    if manual:
        print(f"\nNo public feed, check in browser ({len(manual)}): " + ", ".join(manual))


if __name__ == "__main__":
    main()
