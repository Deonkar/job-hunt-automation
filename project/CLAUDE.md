# job-hunt project

Code and the user's data behind the `job-hunt` skill (`~/.claude/skills/job-hunt/SKILL.md` routes the routines; read that first). Installed to `~/.claude/job-hunt/`. Python 3.10+ via `PYTHONUTF8=1 py -3 ...` (Windows) or `python3`; Word (Windows) or LibreOffice does PDF export.

## Layout
- Shipped by the repo (overwritten on update): `scripts/`, `countries/*.json` (format presets: us, uk, au, de, nl), `examples/` (a made-up person's profile, bullets and variant; a starter company watchlist), `scheduled-tasks/` (routine prompts).
- The user's own (written by `workflows/setup.md`, never committed, never overwritten by an update):
  - `data/profile.json`: who they are, field, skills, experience, targets, `search` filters. `data/bullets.json`: bullet bank per role and project, plus internships. `data/master.docx`: rendered from those two by `scripts/make_master.py`; every tailored resume is cloned from it.
  - `data/candidate.md`, `data/answer-bank.md`: proof points, tiers, never-list; every form answer. `data/config.json`: sheet ids, resume folder, platforms, quotas, standing approvals, schedules.
  - `data/companies.json` (watchlist with each company's job feed: `ats` = greenhouse/lever/ashby/smartrecruiters/workday/amazon, or `chrome` for browser-only), `data/seen.json`, `data/sponsors.json`.
  - `variants/*.json` (one per target role), `state/*.json` (routine state), `out/` (run output), `.env` (FIRECRAWL_API_KEY, TYPESAFE_API_KEY).
- Scripts: `make_master.py` (profile + bullets to master.docx), `build_resume.py` (variant/JD patch + master to a tailored docx; refuses unknown bullets and invented skills), `to_pdf.ps1` (Word: docx to pdf with page counts), `build_all.sh` (every variant and country), `scout.py` (polls feeds, filters by `profile.search`, scores, writes `out/jobs/<date>.json|csv`), `discover_ats.py` (finds each company's feed from a seed list), `jev_verdict.py` (optional "Jev: apply?" sheet column), `rec_connect.py` (records a sent LinkedIn connection).

## Commands
- Tests: `PYTHONUTF8=1 py -3 scripts/test_build_resume.py`, `scripts/test_scout.py`, `scripts/test_jev_verdict.py` (stdlib unittest; they use a made-up candidate, never real data).
- Master: `PYTHONUTF8=1 py -3 scripts/make_master.py`.
- Daily poll: `PYTHONUTF8=1 py -3 scripts/scout.py --days 2`.
- Build: `PYTHONUTF8=1 py -3 scripts/build_resume.py <patch.json> <out.docx> [--country countries/<code>.json]`.

## Rules
Never hand-edit `data/master.docx` (change profile.json / bullets.json and re-run make_master.py) or add skills or metrics the user doesn't have. Add a company: append to `data/companies_seed.json`, run `scripts/discover_ats.py`. Add a country: a new `countries/<code>.json`. Keep tests green after any script change.
