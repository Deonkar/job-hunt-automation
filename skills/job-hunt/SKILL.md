---
name: job-hunt
description: Job-search automation for whoever installed it. Use for any job-hunt setup, run or change: first-time setup interview (resume, current and past jobs, CTC, notice, visa, preferences, EEO answers, Google Sheet, Firecrawl key), scanning company career pages, searching LinkedIn / Indeed / Naukri / Wellfound / YC Work at a Startup / country job portals, scoring JDs, building JD-tailored one-page resumes, applying only with the user's yes, LinkedIn referral and recruiter outreach, weekly rejection cleanup, and the job_sheet Google Sheet. Not for unrelated coding work.
---

# Job hunt

Routines that find jobs for the user, tailor their resume per JD, apply only with their yes, and track everything in one Google Sheet in their own Drive. This file is the router: read only the workflow you are running plus the references it names. Do not load everything.

## First: is the user set up?
If `~/.claude/job-hunt/data/profile.json` does not exist, run `workflows/setup.md` and nothing else, whatever was asked. The same workflow handles "update my profile / CTC / preferences / new job".

## Always read first
- `references/rules.md`: hard rules (approvals, logins, LinkedIn caps, tabs, honesty). Every routine follows them.

## Paths
- **Project** (code + the user's data): `~/.claude/job-hunt/` (its `CLAUDE.md` explains the layout). Run Python as `PYTHONUTF8=1 py -3 ...` (Windows) or `python3 ...` from that folder.
- `data/...` in any file of this skill means `~/.claude/job-hunt/data/...`; `state/...` means `~/.claude/job-hunt/state/...`.
- **The user** is described only in `data/profile.json`, `data/candidate.md` (who they are, proof points, tiers, never-list) and `data/answer-bank.md` (form answers). **Settings** are in `data/config.json`: `sheet_id` and tab gids, `resume_dir`, `platforms`, `quota`, `standing_yes`, `timezone`, `routines`.
- `<resume_dir>` = `config.resume_dir` (default `~/Desktop/job_resumes`). Tailored resumes go to `<resume_dir>/<date>/`.
- JD scoring subagent: `jd-matcher` (Agent tool). Use it to read JDs so the main run's context stays small.
- All times are the user's local time (`config.timezone`).

## Pick the workflow
| Running | Read | Scheduled task (default time) |
|---|---|---|
| First-time setup, or changing profile / pay / preferences | `workflows/setup.md` | none |
| Daily company career-page scan, JD match, tailored resumes, sheet rows | `workflows/company-scan.md` | `company-scout-daily` (08:30) |
| Global search + apply (LinkedIn Easy Apply, Indeed, Naukri, Wellfound, YC Work at a Startup; only those on in `config.platforms`) | `workflows/global-search.md` | `global-job-search` (every 3h, 6h once quota met) |
| Profile refresh (Naukri daily edit if pre-approved; Wellfound and Work at a Startup profiles) | `workflows/profile-refresh.md` | Naukri: `naukri-profile-daily` (09:00); Wellfound / YC: called from global-search |
| LinkedIn referral outreach for the day's top 2 jobs, Gmail drafts | `workflows/referral-outreach.md` | `referral-outreach-daily` (12:00) |
| Recruiter email: the day's best job, up to 2 recruiters' work emails via SignalHire / Apollo, Gmail drafts, Outreach rows | `workflows/recruiter-email.md` | `recruiter-email-daily` (17:00) |
| No-note LinkedIn connections at watchlist companies (only with `standing_yes.linkedin_no_note_connections`) | `workflows/linkedin-connect.md` | `linkedin-connect-daily` (14:00) |
| Sheet triggers: Outreach rows set to Send connection request / Send DM / Send email, Jobs rows set to Approved | `workflows/sheet-actions.md` | `outreach-sheet-actions` (20:00) |
| Country job portals (`config.platforms.country_portals`): shortlist English roles with sponsorship, tailored resumes, Jobs rows, apply on the user's yes | `workflows/country-portals.md` | `country-portals-daily` (18:30) |
| Weekly rejection check, sheet status, resume cleanup | `workflows/weekly-cleanup.md` | `weekly-cleanup` (Sun 10:30) |

## References (load when a workflow says so)
- `references/questionnaire.md`: every setup question and where its answer is stored.
- `references/platforms.md`: search URLs and how each site applies.
- `references/sheet.md`: tab columns, dropdowns, how to append, update and sort rows.
- `references/visa-sponsorship.md`: how to check whether a company sponsors visas before ruling out an abroad role; cache in `data/sponsors.json`.
- `references/resume-tailoring.md`: variants, country presets, JD patches, the "Resume changes" and "Skills to learn" columns.
- `references/progress-band.md`: optional flow-tracker progress band.

## Tools
Load deferred tools with ToolSearch only when the step needs them: Claude in Chrome (`select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__find,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__browser_batch,mcp__claude-in-chrome__form_input`, plus `file_upload` for attachments), Google Sheets ("google sheets append values"), Google Drive ("google drive create file"), Gmail ("gmail create draft"), Indeed ("indeed search jobs"), Firecrawl ("firecrawl scrape").

**Firecrawl** (when `config.firecrawl` is true and its tools are loaded): read public pages (company career pages, JD pages, country portal listings) with Firecrawl scrape instead of opening a Chrome tab; it is faster and keeps Chrome free. Chrome stays for anything behind the user's sign-in (LinkedIn, Naukri, Wellfound, YC) and for every application form.
