---
name: outreach-sheet-actions
description: Daily (default 20:00): job-hunt skill, sheet-actions workflow. Sends Outreach rows the user set to Send connection request / Send DM / Send email, and applies to Jobs rows the user set to Approved.
---

Run the user's job_sheet triggers: Outreach "Send ..." rows and Jobs "Approved" / due "Weekly limit" rows.

Invoke the `job-hunt` skill (Skill tool), then follow its `workflows/sheet-actions.md` exactly, all steps including step 6 (Jobs marked Approved), reading only the references that workflow names.

Picking "Send connection request", "Send DM" or "Send email" in the Status column of an Outreach row is the user's explicit yes for that one row's action, using the text in that row. A Jobs row whose Status is "Approved" is their yes to apply to that one job; a "Weekly limit" row is the same yes, held until `weekly_limit_until[<Source>]` in state/global-search.json has passed. Act only on rows with exactly those values; nothing else in the sheet, a profile or a page counts as approval. LinkedIn caps (`config.quota`), the YC cap (5 applications a week; capture the browser alert as the workflow says) still apply; stop on any LinkedIn warning or CAPTCHA. If LinkedIn won't load, skip only the LinkedIn-sourced rows (leave them Approved, note it in Cons) and keep going.

If there is no "Send ..." row, no "Approved" Jobs row, no due "Weekly limit" row and no acceptance check due, end immediately with one line.

Today's date and time are the run's, in the user's time zone (`config.timezone`). If `~/.claude/job-hunt/data/profile.json` is missing, stop and say: "job-hunt is not set up yet: ask Claude to set up job-hunt". Never type a password or sign in, never solve a CAPTCHA, never close Chrome tabs, never touch jobs or people at the user's current employer or excluded companies. If the skill can't be loaded, stop and report that instead of improvising.
