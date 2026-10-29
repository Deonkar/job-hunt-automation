---
name: naukri-profile-daily
description: Daily (default 09:00): job-hunt skill, profile-refresh workflow, Naukri daily refresh only. One small truthful rotating edit, only if the user turned on that standing yes at setup.
---

Run the user's daily Naukri profile refresh.

First read `~/.claude/job-hunt/data/config.json`: if `platforms.naukri` or `standing_yes.naukri_daily_profile_edit` is not true, end with one line and do nothing. Otherwise invoke the `job-hunt` skill (Skill tool) and follow only the "Naukri daily refresh" section of its `workflows/profile-refresh.md`. State file: ~/.claude/job-hunt/state/global-search.json (profile_edit_date, profile_edit_last).

The standing yes covers only that one edit: swap between the two headlines in `config.naukri_headlines`, move one of the first five key skills one place, or reword one clause of the summary, as the workflow's day rotation says. It must stay truthful: no new skills, numbers or claims. Don't change anything else and don't apply to jobs. If the edit is already done today, end with one line.

Report in two lines: the field changed, before and after, and that it was saved and confirmed.

Today's date and time are the run's, in the user's time zone (`config.timezone`). If `~/.claude/job-hunt/data/profile.json` is missing, stop and say: "job-hunt is not set up yet: ask Claude to set up job-hunt". Never type a password or sign in, never solve a CAPTCHA, never close Chrome tabs, never touch jobs or people at the user's current employer or excluded companies. If the skill can't be loaded, stop and report that instead of improvising.
