"""Find the public job feed behind each company's careers page.

Probes Greenhouse, Lever, Ashby and SmartRecruiters with candidate board slugs, checks
Workday tenants and Amazon, and scans the careers page HTML for ATS links. Writes
data/companies.json; companies with no feed are marked `chrome` (checked in the browser).

Usage: py -3 discover_ats.py [--seed data/companies_seed.json] [--out data/companies.json]
"""
import argparse
import json
import os
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0 (job-hunt watchlist)", "Accept": "application/json"}
ATS_LINK = re.compile(
    r"(boards(?:-api)?\.greenhouse\.io/(?:embed/job_board\?for=)?([\w-]+)"
    r"|job-boards\.greenhouse\.io/([\w-]+)"
    r"|jobs\.lever\.co/([\w-]+)"
    r"|jobs\.ashbyhq\.com/([\w.-]+)"
    r"|careers\.smartrecruiters\.com/([\w-]+)"
    r"|([\w-]+)\.wd\d+\.myworkdayjobs\.com)", re.I)


def fetch(url, data=None, timeout=20):
    body = json.dumps(data).encode() if data is not None else None
    headers = dict(UA, **({"Content-Type": "application/json"} if body else {}))
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    return raw.decode("utf-8", "replace")


def count_jobs(ats, slug):
    """Return the number of open jobs on a board, or None if the board doesn't exist."""
    try:
        if ats == "greenhouse":
            return len(json.loads(fetch(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"))["jobs"])
        if ats == "lever":
            d = json.loads(fetch(f"https://api.lever.co/v0/postings/{slug}?mode=json"))
            return len(d) if isinstance(d, list) else None
        if ats == "ashby":
            d = json.loads(fetch(f"https://api.ashbyhq.com/posting-api/job-board/{slug}"))
            return len(d["jobs"]) if "jobs" in d else None
        if ats == "smartrecruiters":
            d = json.loads(fetch(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings?limit=1"))
            return d.get("totalFound") or None  # unknown companies return 0, not 404
    except Exception:
        return None


def workday_count(host, tenant, site):
    try:
        d = json.loads(fetch(f"https://{host}/wday/cxs/{tenant}/{site}/jobs",
                             {"appliedFacets": {}, "limit": 1, "offset": 0, "searchText": ""}))
        return d.get("total")
    except Exception:
        return None


def amazon_count():
    try:
        return json.loads(fetch("https://www.amazon.jobs/en/search.json?result_limit=1"))["hits"]
    except Exception:
        return None


def slug_candidates(c):
    base = re.sub(r"\(.*?\)", "", c["name"]).strip().lower()
    out = list(c.get("slugs", []))
    for s in (re.sub(r"[^a-z0-9]", "", base), re.sub(r"[^a-z0-9]+", "-", base).strip("-")):
        if s not in out:
            out.append(s)
    return out


def links_on_page(url):
    try:
        html = fetch(url)
    except Exception:
        return []
    found = []
    for m in ATS_LINK.finditer(html):
        g = m.groups()
        if g[1] or g[2]:
            found.append(("greenhouse", g[1] or g[2]))
        elif g[3]:
            found.append(("lever", g[3]))
        elif g[4]:
            found.append(("ashby", g[4]))
        elif g[5]:
            found.append(("smartrecruiters", g[5]))
        elif g[6]:
            found.append(("workday-host", g[6]))
    return list(dict.fromkeys(found))


def discover(c):
    row = {k: c[k] for k in ("name", "segment", "region", "careers")}
    if c.get("ats") == "amazon":
        return dict(row, ats="amazon", board="amazon", open_jobs=amazon_count())
    if c.get("workday"):
        host, tenant, site = c["workday"]
        n = workday_count(host, tenant, site)
        if n is not None:
            return dict(row, ats="workday", board=f"{host}|{tenant}|{site}", open_jobs=n)
    candidates = [(a, s) for a, s in links_on_page(c["careers"]) if a != "workday-host"]
    candidates += [(a, s) for s in slug_candidates(c)
                   for a in ("greenhouse", "lever", "ashby", "smartrecruiters")]
    best = None
    for ats, slug in dict.fromkeys(candidates):
        n = count_jobs(ats, slug)
        if n is not None and (best is None or n > best[2]):
            best = (ats, slug, n)
    if best:
        return dict(row, ats=best[0], board=best[1], open_jobs=best[2])
    return dict(row, ats="chrome", board=None, open_jobs=None)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", default=os.path.join(root, "data", "companies_seed.json"))
    ap.add_argument("--out", default=os.path.join(root, "data", "companies.json"))
    a = ap.parse_args()
    seed = json.load(open(a.seed, encoding="utf-8"))
    with ThreadPoolExecutor(16) as pool:
        rows = list(pool.map(discover, seed))
    json.dump(rows, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    for r in rows:
        print(f"{r['ats']:15} {str(r['open_jobs']):>6}  {r['name']}  {r['board'] or ''}")


if __name__ == "__main__":
    main()
