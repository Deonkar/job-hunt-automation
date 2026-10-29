---
name: recruiter-email-daily
description: Daily (default 17:00): job-hunt skill, recruiter-email workflow. Picks today's single best job, finds up to 2 recruiters there, gets work emails via the user's SignalHire/Apollo extension, drafts emails as Outreach rows for the user's approval.
---

Run the user's daily recruiter email for the day's best job.

Invoke the `job-hunt` skill (Skill tool), then follow its `workflows/recruiter-email.md` exactly, reading only the references that workflow names. If `config.recruiter_email_tools` is empty, end with one line.

Use only work emails at the company's own domain that the tool doesn't mark as guessed; never collect phone numbers or personal emails, never guess an address, at most 2 reveals per tool per run. Nothing is sent by this run: it creates Gmail drafts and Outreach rows with Status "Awaiting approval"; the user approves by picking "Send email" on a row, and the evening sheet-actions routine sends it with the tailored resume attached.

Today's date and time are the run's, in the user's time zone (`config.timezone`). If `~/.claude/job-hunt/data/profile.json` is missing, stop and say: "job-hunt is not set up yet: ask Claude to set up job-hunt". Never type a password or sign in, never solve a CAPTCHA, never close Chrome tabs, never touch jobs or people at the user's current employer or excluded companies. If the skill can't be loaded, stop and report that instead of improvising.
