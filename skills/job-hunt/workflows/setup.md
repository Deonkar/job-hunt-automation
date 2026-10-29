# Workflow: setup (first run, or "update my profile / CTC / preferences")

Runs when `~/.claude/job-hunt/data/profile.json` is missing, or when the user asks to set up, re-run setup, or change a section ("update my expected CTC", "add Germany", "new job"). For a change, run only the rounds it touches, then step 6 if the resume content changed.

Read: `references/rules.md`, `references/questionnaire.md`. Everything the user tells you is personal data: it lives only in `~/.claude/job-hunt/` on this machine (`data/`, `.env`, `state/`, `out/`) and is never written into the skill folder, a repo, a commit or a public page.

Before starting, say in two lines what setup does (about 15-25 minutes of questions, then it builds the master resume, the Google Sheet and the schedules) and that any question can be skipped and answered later.

## 0. Check the machine
Run and report one line each, fixing what you can with the user's yes:
- Project folder: `~/.claude/job-hunt/` with `scripts/`, `countries/`, `examples/`. Missing: the skill was installed without the project; point to the README's install step.
- `py -3 --version` (Windows) or `python3 --version`: 3.10+. `py -3 -c "import docx"`: if it fails, offer `py -3 -m pip install python-docx`.
- PDF export: Microsoft Word (Windows: `scripts/to_pdf.ps1`) or LibreOffice (`soffice --headless --convert-to pdf`). Neither: tailored resumes stay .docx; say so.
- Connectors and tools present in this session: Google Sheets, Google Drive, Gmail, Claude in Chrome, Indeed, Firecrawl, scheduled tasks. List what is missing and what each one unlocks; nothing is required except Sheets.
- Create `~/.claude/job-hunt/data/`, `state/`, `out/`, `variants/` if missing.

## 1. Resume first (round 1)
Ask for the resume file (or pasted text) before anything else, read it in full, and pre-fill every later answer you can from it. Then ask round 1's remaining questions.

## 2. Interview (rounds 2-11)
One round per message, in order, from `references/questionnaire.md`. For each question show the value read from the resume (if any) as the default, so the user mostly confirms. Use AskUserQuestion for choice questions (yes / no, ranges, platforms, routines). Rules:
- Never guess a missing answer. Leave it as `{{ask}}` in the file; the routines ask it the first time a form needs it and then store it.
- Numbers (CTC, years, notice) are written exactly as the user gives them, with the currency and unit.
- Round 8 stories: draft each from the resume in 2-4 sentences, show the drafts together, write only what the user approves.
- Round 9 is optional as a whole: offer "skip this round" first.
- Keys (round 10): ask the user to paste them into chat only if they are happy to; write them straight to `~/.claude/job-hunt/.env` (`FIRECRAWL_API_KEY=...`, `TYPESAFE_API_KEY=...`), never echo them back, never put them in any other file. Offer the alternative of editing `.env` themselves.

## 3. Write the data files
From the answers, write (show a short summary of each, not the whole file, and ask "anything to fix?"):
- `data/profile.json`: schema as `examples/profile.json`. `experience.full_time[]` and `projects[]` each get a short `key`.
- `data/bullets.json`: schema as `examples/bullets.json`. Bullets copy the resume's facts and numbers exactly; `short` alternates may only shorten. `experience` and `projects` use the same keys and order as profile.json.
- `data/candidate.md` from `~/.claude/skills/job-hunt/templates/candidate.md`; `data/answer-bank.md` from `templates/answer-bank.md`; `data/config.json` from `templates/config.json`. Replace every `{{...}}` with the answer or `{{ask}}`; delete the template comments.
- `data/companies_seed.json`: the user's dream companies plus, if they want a starter list, the relevant entries of `examples/companies_seed.json` (it leans to India and remote-first tech). Then `PYTHONUTF8=1 py -3 scripts/discover_ats.py --seed data/companies_seed.json --out data/companies.json` to find each company's public job feed. Never add the employer or excluded companies.
- `data/seen.json` `[]`, `data/sponsors.json` `{}`.
- `countries/*.json`: keep the presets for the countries they target. If they already have the right to work in a country, delete that preset's `work_auth` line. Add `replace` pairs for phrases that should change abroad (local currency first, degree names spelled out).
- Optional, Firecrawl: if the user gave a key and has no Firecrawl tools in Claude Code yet, show this command for them to run (it stores the key in their Claude config, not in this project):
  `claude mcp add firecrawl -e FIRECRAWL_API_KEY=<their key> -- npx -y firecrawl-mcp`
  Set `config.firecrawl` to true once the tools show up.

## 4. Master resume and variants
- `PYTHONUTF8=1 py -3 scripts/make_master.py` writes `data/master.docx` from profile.json + bullets.json. Render it to PDF and show the page count. Ask the user to open the PDF and check every line; fix the data files (never the docx) and rebuild until they say it is right.
- One variant per target in `profile.targets` into `variants/<archetype>.json` (schema `examples/variants/backend.json`: title, summary, skills_order, skills_items, experience bullet ids per role, projects, projects_order, internships). Summaries may only re-state resume facts.
- `bash scripts/build_all.sh` (Word) or build + LibreOffice by hand; every PDF must be 1 page (2 allowed for 8+ years of experience if the user says so). Copy the base PDFs to `<resume_dir>/base/`.

## 5. The tracking sheet (in the user's own Google Drive)
- Create a spreadsheet named `job_sheet` with the Google Drive connector (`create_file`, mimeType `application/vnd.google-apps.spreadsheet`). If that isn't available, ask the user to open https://sheets.new, name it `job_sheet` and paste its URL.
- With the Sheets connector (`update_spreadsheet`), set it up exactly as `references/sheet.md` describes: rename the first tab to `Jobs` (gid 0) and add `Outreach` and `Companies`; header rows; freeze row 1; Jobs status dropdown (strict list) on O and its colour rules; hide column P; Outreach status dropdown on I and its colours; Companies filled from `data/companies.json`.
- Read the tabs back with `get_spreadsheet` and store `sheet_id`, `outreach_gid`, `companies_gid` in `data/config.json`.

## 6. Verify
- `PYTHONUTF8=1 py -3 scripts/test_build_resume.py`, `test_scout.py`, `test_jev_verdict.py`: all OK.
- `PYTHONUTF8=1 py -3 scripts/scout.py --days 3 --no-mark`: report how many feeds and matches it found (dry run, nothing marked seen).
- If `.env` has a TypeSafe key: one `jev_verdict.py` call on a sample job; otherwise note "Jev column off".

## 7. Schedules (only with the user's yes)
Show the routines table from `SKILL.md` with the times from `config.routines` in the user's time zone, plus which ones are off (platforms they didn't pick, no Gmail, no LinkedIn). On their yes, create each chosen routine with the scheduled-tasks connector (`create_scheduled_task`), using the prompt in `~/.claude/job-hunt/scheduled-tasks/<name>/SKILL.md` and that schedule. Never create a routine they didn't pick.

## 7b. Profiles (round 12)
For each profile the user picked, run `workflows/profile-refresh.md` "Full optimization" (LinkedIn through `linkedin-profile-optimizer` when installed). Every change is shown before / after and saved only on their yes.

## 8. Report
What was written (file names only, no personal values), what is still `{{ask}}`, sheet link, base resumes folder, routines scheduled, and the first thing to try: "run the company scan now".
