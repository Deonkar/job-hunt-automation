---
name: company-scout-daily
description: Daily (default 08:30): job-hunt skill, company-scan workflow (career-page feeds + browser companies, jd-matcher scoring, tailored resumes, Jobs tab rows).
---

Run the user's daily company careers scan.

Invoke the `job-hunt` skill (Skill tool), then follow its `workflows/company-scan.md` exactly, reading only the references that workflow names. Use the `jd-matcher` agent for the JD scoring step. Nothing is submitted without the user's yes for that exact job.

Today's date and time are the run's, in the user's time zone (`config.timezone`). If `~/.claude/job-hunt/data/profile.json` is missing, stop and say: "job-hunt is not set up yet: ask Claude to set up job-hunt". Never type a password or sign in, never solve a CAPTCHA, never close Chrome tabs, never touch jobs or people at the user's current employer or excluded companies. If the skill can't be loaded, stop and report that instead of improvising.
