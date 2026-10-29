"""Ask Jev (TypeSafe System One) whether the candidate should apply to each job. Optional:
the Jobs sheet's "Jev: apply?" column stays "Jev: no key" without a TypeSafe key.

Usage: py -3 jev_verdict.py JOBS.json [--out VERDICTS.json]
JOBS.json is a list of job objects (company, role, location, region, posted, source,
pros, cons, skills_to_learn, link, and jd text when the run has it). Prints one line
per job and writes [{company, role, link, jev}] where jev is the Jobs sheet cell,
e.g. "Yes (0.82)" or "No (0.18): experience gap, location".

The key comes from TYPESAFE_API_KEY, else from the project's .env file (written at setup).
A failed call gives the cell "Jev error: <reason>" and never stops the run.
"""
import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE = os.path.join(ROOT, "data", "profile.json")
CANDIDATE_MD = os.path.join(ROOT, "data", "candidate.md")
ANSWER_BANK = os.path.join(ROOT, "data", "answer-bank.md")
ENV_FILE = os.path.join(ROOT, ".env")
ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
APPLY_AT = 0.5    # the candidate decides from the cell; yes/no only needs the midpoint
BLOCKER_AT = 0.6  # name a blocker in the cell only when Jev leans clearly yes on it



def questions(home):
    """Jev's typed questions; `home` is the country the candidate lives in (profile.json home_country)."""
    return {
        "apply": {
            "type": "noul",
            "instructions": "Should `candidate` apply to `job`?",
            "criteria": {
                "true": "A realistic, worthwhile application: the candidate meets or nearly meets the experience "
                        "asked, their stack or domain overlaps the role, the location or remote/visa terms are open "
                        f"to someone based in {home}, the level matches their target level, and the role fits "
                        "their target roles and pay expectations.",
                "false": "Not worth applying: the experience asked is well above theirs, the level is far above or "
                         "below their target, the location needs a work permit they lack, the work is far from "
                         "their stack, or the pay or contract terms are clearly below what they want.",
            },
        },
        "experience_gap": {
            "type": "noul",
            "instructions": "`job` asks for clearly more experience than `candidate` has "
                            "(e.g. 3+ years when they have under 2 years full-time).",
        },
        "location_blocked": {
            "type": "noul",
            "instructions": f"`job`'s location or work-authorization terms rule out a candidate based in {home} "
                            "(needs existing work authorization abroad, US-only hiring, or on-site abroad "
                            "without visa sponsorship).",
        },
        "stack_mismatch": {
            "type": "noul",
            "instructions": "`job`'s core stack or domain is mostly outside `candidate`'s skills.",
        },
    }
BLOCKER_NAMES = {"experience_gap": "experience gap", "location_blocked": "location", "stack_mismatch": "stack mismatch"}


def full_time_months(start, today):
    y, m = (int(x) for x in start.split("-"))
    return (today.year - y) * 12 + today.month - m


def total_full_time_months(roles, today):
    total = 0
    for r in roles:
        end = dt.date.fromisoformat(r["end"] + "-01") if r.get("end") else today
        total += full_time_months(r["start"], end)
    return total


def build_state(job, candidate_md, profile, today):
    months = total_full_time_months(profile["experience"]["full_time"], today)
    return {
        "candidate": {
            "full_time_experience": f"{months // 12} year {months % 12} months",
            "profile": candidate_md,
            "skills": profile["skills"],
        },
        "job": job,
    }


def cell(answers):
    p = answers["apply"]["noul"]
    out = f"{'Yes' if p >= APPLY_AT else 'No'} ({p:.2f})"
    blockers = [name for q, name in BLOCKER_NAMES.items() if answers[q]["noul"] > BLOCKER_AT]
    return out + (": " + ", ".join(blockers) if blockers else "")


def key_from_env_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                k, _, v = line.strip().partition("=")
                if k == "TYPESAFE_API_KEY":
                    return v.strip().strip("\"'") or None
    except OSError:
        return None
    return None


def api_key():
    return os.environ.get("TYPESAFE_API_KEY") or key_from_env_file(ENV_FILE)


def ask(state, key, qs):
    body = json.dumps({"model": MODEL, "state": state, "questions": qs}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return cell(json.load(r)["answers"])
    except urllib.error.HTTPError as e:
        return f"Jev error: HTTP {e.code}"
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as e:
        return f"Jev error: {type(e).__name__}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs")
    ap.add_argument("--out")
    a = ap.parse_args()
    with open(a.jobs, encoding="utf-8") as f:
        jobs = json.load(f)
    key = api_key()
    if not key:
        sys.exit("No TYPESAFE_API_KEY: set it in the environment or in the project's .env file")
    with open(PROFILE, encoding="utf-8") as f:
        profile = json.load(f)
    notes = ""
    for path in (CANDIDATE_MD, ANSWER_BANK):
        with open(path, encoding="utf-8") as f:
            notes += f.read() + "\n"
    today = dt.date.today()
    qs = questions(profile.get("home_country", "their home country"))
    with ThreadPoolExecutor(8) as pool:
        cells = list(pool.map(lambda j: ask(build_state(j, notes, profile, today), key, qs), jobs))
    out = [{"company": j.get("company"), "role": j.get("role"), "link": j.get("link"), "jev": c}
           for j, c in zip(jobs, cells)]
    for o in out:
        print(f"{o['jev']:<45} {o['company']} | {o['role']}")
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
