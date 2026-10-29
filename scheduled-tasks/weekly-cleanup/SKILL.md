---
name: weekly-cleanup
description: Sundays (default 10:30): job-hunt skill, weekly-cleanup workflow (find rejections in Gmail / LinkedIn / Naukri, mark them in the sheet, move their tailored resumes aside after the user's yes).
---

Run the user's weekly rejection check and cleanup.

Invoke the `job-hunt` skill (Skill tool), then follow its `workflows/weekly-cleanup.md` exactly, reading only the references that workflow names. Sheet status updates and moving resume files happen only after the user's yes for the proposed list.

Today's date and time are the run's, in the user's time zone (`config.timezone`). If `~/.claude/job-hunt/data/profile.json` is missing, stop and say: "job-hunt is not set up yet: ask Claude to set up job-hunt". Never type a password or sign in, never solve a CAPTCHA, never close Chrome tabs, never touch jobs or people at the user's current employer or excluded companies. If the skill can't be loaded, stop and report that instead of improvising.
