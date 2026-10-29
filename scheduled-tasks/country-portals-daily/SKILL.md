---
name: country-portals-daily
description: Daily (default 18:30): job-hunt skill, country-portals workflow. Refreshes the country job portals the user picked at setup, shortlists roles they can do (language, sponsorship), builds tailored resumes, adds Jobs rows and applies only with the user's yes.
---

Run the user's daily country job-portal search.

Invoke the `job-hunt` skill (Skill tool), then follow its `workflows/country-portals.md` exactly, reading only the references that workflow names (the portal list is in `references/platforms.md`, section "Country portals"; only portals in `config.platforms.country_portals` are used). State file: ~/.claude/job-hunt/state/country-portals.json (create it if missing).

This is not a yes to submit anything: every application needs the user's explicit yes for that exact job in chat, or a Jobs row they set to "Approved". Log a portal that needs sign-in instead of signing in, and drop any role that needs a language the user doesn't speak at the level asked.

Today's date and time are the run's, in the user's time zone (`config.timezone`). If `~/.claude/job-hunt/data/profile.json` is missing, stop and say: "job-hunt is not set up yet: ask Claude to set up job-hunt". Never type a password or sign in, never solve a CAPTCHA, never close Chrome tabs, never touch jobs or people at the user's current employer or excluded companies. If the skill can't be loaded, stop and report that instead of improvising.
