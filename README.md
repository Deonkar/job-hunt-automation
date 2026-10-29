# job-hunt-automation

A Claude Code skill that runs your job search: it scans company career pages and job boards, scores each job description against your profile, builds a one-page resume tailored to each job, applies only after you say yes, optimizes your LinkedIn / Naukri / Indeed profiles, drafts referral and recruiter outreach, and tracks everything in a Google Sheet in your own Drive.

It works for any field: software, data, design, sales, HR and recruiting, marketing, finance, operations and more. Nothing about you ships in this repo. The first time you use it, Claude interviews you and keeps your answers on your machine only.

## Install

```bash
git clone https://github.com/Deonkar/job-hunt-automation.git
```

```bash
bash job-hunt-automation/install.sh
```

Windows: run it from Git Bash. The installer copies the skill to `~/.claude/skills/job-hunt`, the `jd-matcher` agent to `~/.claude/agents/`, and the scripts to `~/.claude/job-hunt/`. Re-run it to update; it never touches your data.

Then open Claude Code and say **"set up job-hunt"**.

## What setup asks (about 15-25 minutes, skip anything)

Setup reads your resume first and pre-fills what it can, then asks in rounds. These are the questions real application forms and recruiter screens ask:

1. **Resume and identity:** resume file, name, email, phone, city, links, pronouns, your field.
2. **Current job:** company, exact title, start date, awards, notice period (negotiable? serving?), reason for change.
3. **Past jobs, internships, education:** titles as on offer letters (background checks), degree, grades, certifications, spoken languages.
4. **Pay:** currency, current pay (fixed, variable, stock), your floor, expected range per company type, abroad salary answer, contract rate.
5. **What you want:** target roles and level, title words to include and skip, years of experience, industries, dream and never companies.
6. **Location and work authorization:** remote / hybrid / on-site, 5-day office, relocation at home and abroad, citizenship, visa sponsorship, shifts, travel, interview availability, earliest start.
7. **Skills, honestly:** confirmed skills list, years per tool, domain years, self-ratings forms ask (sales quota attainment, DSA rating, hiring volume...).
8. **Stories:** your strongest results, most impactful work, a measured result, cross-team project, how you use AI tools, motivation, a failure. Claude drafts them from your resume and you approve.
9. **Self-identification and legal (optional, "Prefer not to say" is fine):** gender, race / ethnicity, disability, veteran status, relatives at the company, non-compete, consent policy.
10. **Tools and keys:** job sites, Google Sheets / Drive / Gmail connectors, Firecrawl API key (optional), TypeSafe key (optional), SignalHire / Apollo (optional), resume folder.
11. **Pace and permissions:** applications a day, LinkedIn limits, which routines to schedule and when, any standing approvals.
12. **Profiles:** which of LinkedIn, Naukri, Indeed, Wellfound and YC Work at a Startup to optimize now.

Then it writes your profile, renders your master resume (you check the PDF), builds one resume variant per target role, creates the `job_sheet` Google Sheet in your Drive, runs the tests, and schedules the routines you picked.

## Where your data lives

Everything personal stays in `~/.claude/job-hunt/` on your computer and never goes into this repo:

| Path | What |
|---|---|
| `data/profile.json`, `data/bullets.json` | Your profile, skills and resume bullets (source of every resume) |
| `data/master.docx` | Your master resume, rendered from the two files above |
| `data/candidate.md`, `data/answer-bank.md` | Proof points and preferences; your answers to application forms |
| `data/config.json` | Sheet ids, resume folder, platforms, quotas, schedules |
| `.env` | API keys (Firecrawl, TypeSafe) |
| `state/`, `out/`, `variants/` | Routine state, run output, your resume variants |

Keys go in `.env` only. The `.gitignore` here also blocks `project/data`, `state`, `out`, `.docx` and `.pdf`, so nothing slips in if you run it from the repo.

## Safety rules it always follows

- Nothing is submitted, sent or published without your yes for that exact item (or a sheet dropdown you set: "Approved", "Send DM"...).
- It never signs in, never types a password, never solves a CAPTCHA.
- It never applies to your current employer or contacts anyone there.
- It never invents a skill, number or answer. Skills a job wants that you lack go in a "Skills to learn" column, never on your resume.
- It stays under LinkedIn's limits (5 Easy Apply a day, 15 connection requests a day, 100 a week) and stops at the first warning.

## Requirements

- Claude Code with the **Google Sheets** connector (required). Optional: Google Drive, Gmail, Claude in Chrome, Indeed, scheduled tasks.
- Python 3.10+ with `python-docx` (`pip install python-docx`).
- Microsoft Word (Windows) or LibreOffice for PDF export.
- Optional: a [Firecrawl](https://firecrawl.dev) API key, so career pages and job descriptions are read without opening Chrome tabs. Setup stores it in `.env` and shows the one command that adds Firecrawl to Claude Code.

## LinkedIn profile optimization: credit

Full LinkedIn profile audits use **`linkedin-profile-optimizer`** from [sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills) by Sergey Bulaev (MIT license). It is not copied into this repo. Setup offers to install it from its source, so you get its updates:

```text
/plugin marketplace add sergebulaev/linkedin-skills
/plugin install linkedin-skills@linkedin-skills
```

Without it, the skill uses its own built-in LinkedIn checklist. Naukri, Indeed, Wellfound and YC Work at a Startup profiles use this repo's own `workflows/profile-refresh.md`.

## Layout

| Folder | Installed to | What |
|---|---|---|
| `skills/job-hunt/` | `~/.claude/skills/job-hunt/` | The skill: `SKILL.md` router, `workflows/` (setup and every routine), `references/`, `templates/` |
| `agents/jd-matcher.md` | `~/.claude/agents/` | Subagent that scores a JD against your profile and returns a JSON verdict |
| `project/` | `~/.claude/job-hunt/` | Scripts (resume builder, feed scout), country resume presets, examples |
| `scheduled-tasks/` | `~/.claude/job-hunt/scheduled-tasks/` | Prompts for the daily and weekly routines; setup schedules the ones you pick |

Tests use a made-up person: `py -3 -m unittest discover -s project/scripts`
