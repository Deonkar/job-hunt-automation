---
name: linkedin-connect-daily
description: Daily (default 14:00): job-hunt skill, linkedin-connect workflow. No-note connection requests to peers and recruiters at watchlist companies, only if the user gave that standing yes at setup; 12 per run at most.
---

Run the user's daily no-note LinkedIn connection round.

First read `~/.claude/job-hunt/data/config.json`: if `standing_yes.linkedin_no_note_connections` is not true, end with one line and do nothing. Otherwise invoke the `job-hunt` skill (Skill tool) and follow its `workflows/linkedin-connect.md` exactly. That standing yes covers only plain connection requests with no note to people in the user's function and HR or recruiters at watchlist companies: never add a note and never send a message.

Safety: respect the shared LinkedIn cap (`config.quota`, default 15 connection requests a day and 100 a week across all routines, counted in state/outreach.json), one action at a time. Stop at once on any LinkedIn warning, limit notice or CAPTCHA.

When every watchlist company is done, report "All watchlist companies done: disable linkedin-connect-daily" and do nothing else.

Today's date and time are the run's, in the user's time zone (`config.timezone`). If `~/.claude/job-hunt/data/profile.json` is missing, stop and say: "job-hunt is not set up yet: ask Claude to set up job-hunt". Never type a password or sign in, never solve a CAPTCHA, never close Chrome tabs, never touch jobs or people at the user's current employer or excluded companies. If the skill can't be loaded, stop and report that instead of improvising.
