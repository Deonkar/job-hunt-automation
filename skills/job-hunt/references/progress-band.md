# Progress band (flow-tracker)

Optional. If a `mcp__flow-tracker__update_flow` tool exists and accepts lane "jobsearch", report progress; otherwise skip this file silently.

- First call: `feature` (below), `title`, `lane: "jobsearch"`, `links` (below), and steps the routine skips as `skipped`.
- Steps: profile-refresh, pages-refresh, data-scan, jd-match, resume-update, sheet-update, apply. Mark `ongoing` when a step starts, `done` when it ends, `blocked` while waiting on the user, with a short note.

Company scan and global search share ONE entry per day so the band shows the whole day: never mark the other routine's steps as skipped, never reset; just mark your own steps. A step another routine already finished goes back to `ongoing` while you redo it, then `done` again, so the band always shows what is running now.

| Routine | feature | title | its steps |
|---|---|---|---|
| company-scan | job-search-<YYYY-MM-DD> | Daily job search | pages-refresh, data-scan, jd-match, resume-update, sheet-update |
| global-search | job-search-<YYYY-MM-DD> | Daily job search | profile-refresh, data-scan, jd-match, resume-update, apply, sheet-update |
| country-portals | job-search-<YYYY-MM-DD> | Daily job search | pages-refresh, data-scan, jd-match, resume-update, sheet-update, apply |
| referral-outreach | referral-<YYYY-MM-DD> | Referral outreach | all but jd-match (people chosen) and apply (sent) |
| weekly-cleanup | cleanup-<YYYY-MM-DD> | Weekly cleanup | all but data-scan (inbox/status check) and sheet-update |

Links (label + url, http(s) or file:///): always "Jobs sheet" `https://docs.google.com/spreadsheets/d/<sheet_id>/edit#gid=0` and "Resumes" `file:///<resume_dir>`; add routine-specific ones (today's CSV, top 3 resumes, platform profiles, Outreach tab `...#gid=<outreach_gid>`).
