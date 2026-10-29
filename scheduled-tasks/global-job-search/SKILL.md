---
name: global-job-search
description: Every 3h (6h once the daily quota is met), 06:00-24:00: job-hunt skill, global-search workflow (the job boards on in config: LinkedIn Easy Apply, Indeed, Naukri, Wellfound, YC Work at a Startup; applies only with the user's yes).
---

Run the user's global job search.

Invoke the `job-hunt` skill (Skill tool), then follow its `workflows/global-search.md` exactly, reading only the references each workflow names. Do the pace check in step 0 before loading anything else. State file: ~/.claude/job-hunt/state/global-search.json. Every application needs the user's explicit yes for that exact job in chat, or a Jobs row they set to "Approved".

Today's date and time are the run's, in the user's time zone (`config.timezone`). If `~/.claude/job-hunt/data/profile.json` is missing, stop and say: "job-hunt is not set up yet: ask Claude to set up job-hunt". Never type a password or sign in, never solve a CAPTCHA, never close Chrome tabs, never touch jobs or people at the user's current employer or excluded companies. If the skill can't be loaded, stop and report that instead of improvising.
