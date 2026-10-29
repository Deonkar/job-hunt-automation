# Workflow: profile optimization and refresh (LinkedIn, Naukri, Indeed, Wellfound, YC)

Read: `references/rules.md`, `data/candidate.md`, `data/profile.json`. Works for any field (tech, sales, HR, marketing, finance, operations...): write for the user's own field and target roles from `profile.targets`, using the words recruiters in that field search for.

Every edit is shown as before / after and made only after the user's yes (rules.md 2), except the daily Naukri edit when `config.standing_yes.naukri_daily_profile_edit` is on. Profile facts come only from `data/candidate.md`, `data/profile.json` and `data/bullets.json`: no new skills, numbers, titles or dates. Use Claude in Chrome, signed in by the user; a login page means stop and ask them to sign in (rules.md 1).

State: `state/global-search.json` keys `profiles_checked` (`{"linkedin","naukri","indeed","wellfound","waas": "YYYY-MM-DD"}`), `profile_edit_date`, `profile_edit_last`.

## Full optimization (on request, at setup round 12, and every 30 days per profile)
Read the live profile with `get_page_text`, score each section pass / needs work / fail, then propose one batch of edits per profile.

### LinkedIn
- **If the `linkedin-profile-optimizer` skill is installed** (from the MIT-licensed bundle by Sergey Bulaev, https://github.com/sergebulaev/linkedin-skills): invoke it with the Skill tool and give it the profile text plus `data/candidate.md`, the target roles, and this instruction: "facts only from these files". Use its scorecard and rewrites; it covers headline, About, Featured, banner, photo, Experience, Skills, custom URL and recommendations.
- **If it is not installed**, offer it once: in Claude Code, `/plugin marketplace add sergebulaev/linkedin-skills` then `/plugin install linkedin-skills@linkedin-skills`. If the user declines, use this checklist instead:
  - Headline (220 chars): target role + 2-3 searchable skills or domains + one proof point. Not "Seeking opportunities".
  - About: hook line, 3-4 proof points with numbers, what they want next, how to reach them. First person, no buzzwords.
  - Experience: each role's title exactly as on the offer letter, 2-4 bullets from `bullets.json`, the employer's LinkedIn page linked.
  - Skills: top 5 pinned = the skills most JDs for their target roles ask for that they really have (from `profile.skills`).
  - Open to Work: job titles = target roles, locations and work mode from the answer bank; "recruiters only" unless they chose public. Never visible to the current employer's recruiters by default.
  - Custom URL, a professional photo and a banner they choose themselves (never generated faces); Featured with 1-3 work samples if their field has them.
- Never turn on Open to Work, change the headline or post anything without the user's yes for that exact change.

### Naukri (India)
Profile `https://www.naukri.com/mnjuser/profile`. Check and propose:
- Resume headline (up to 250 chars): target role, years, top skills, one result. Store two truthful versions in `config.naukri_headlines` for the daily rotation.
- Key skills: the 8-15 skills recruiters filter on for their target roles, all from `profile.skills`; most important first.
- Profile summary, employment (titles and dates exact, notice period from the answer bank), education, IT / tool skills with years, projects (optional), desired career profile: role, industry, job type, preferred locations, expected CTC (from the answer bank, the floor or the lower end of the range), notice period.
- Upload the current master PDF as the profile resume only with the user's yes.
- Personal details (DOB, gender, category, languages) only from the answer bank; leave blank what it doesn't have.

### Indeed
Profile `https://profile.indeed.com/`. Propose: headline and summary (same facts as LinkedIn), work experience and education exact, skills from `profile.skills`, job preferences (titles, pay floor, work mode, locations, "ready to work" on or off as the user says), and the uploaded resume (master PDF, after a yes). Keep the profile private or public as the user chose.

### Wellfound (startups)
`https://wellfound.com/profile/edit`: headline, bio (3-4 lines from the proof points), current and past roles with correct dates, skills (from profile.json, most relevant first), education, location and remote / relocation, job preferences (target roles, experience band, locations, visa needed abroad), links.

### YC Work at a Startup
`https://www.workatastartup.com/` (candidate profile): role, experience, skills, location, remote / visa preferences, links, a short "what I'm looking for". Don't use `ycombinator.com/apply` (that is YC's founder application).

After each profile: show the batch, apply the approved items, reload and confirm they show, set `profiles_checked.<site>` = today.

## Naukri daily refresh (own task `naukri-profile-daily`; only when `config.standing_yes.naukri_daily_profile_edit` is on and the platform is on)
Naukri ranks recently updated profiles higher in recruiter searches, so one small truthful edit a day keeps the profile visible. Skip if `profile_edit_date` is today. Open the profile and make ONE edit, rotating by day of year % 3: 0 = swap the resume headline between the two in `config.naukri_headlines` (whichever isn't there now); 1 = move one of the first five key skills one place (same skills, nothing added or removed); 2 = reword one clause of the profile summary without changing any fact, number or skill. Save, reload and confirm the change shows. Set `profile_edit_date` = today and `profile_edit_last` = {date, field, before, after}. On a login page, CAPTCHA or error: change nothing, report it (rules.md 1).
