---
name: referral-outreach-daily
description: Daily (default 12:00): job-hunt skill, referral-outreach workflow (people for the top 2 jobs, connection notes, DMs with resume, Gmail drafts; sends only what the user approves).
---

Run the user's daily LinkedIn referral outreach.

Invoke the `job-hunt` skill (Skill tool), then follow its `workflows/referral-outreach.md` exactly, reading only the references that workflow names. Nothing is sent without the user's explicit yes for that item. Respect the shared LinkedIn caps in `config.quota` and stop on any LinkedIn warning.

Today's date and time are the run's, in the user's time zone (`config.timezone`). If `~/.claude/job-hunt/data/profile.json` is missing, stop and say: "job-hunt is not set up yet: ask Claude to set up job-hunt". Never type a password or sign in, never solve a CAPTCHA, never close Chrome tabs, never touch jobs or people at the user's current employer or excluded companies. If the skill can't be loaded, stop and report that instead of improvising.
