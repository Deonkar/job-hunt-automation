# Workflow: sheet actions (Outreach "Send ..." triggers, Jobs "Approved")

Read: `references/rules.md`, `references/sheet.md`. Read nothing else unless there is work.

The user approves from the job_sheet Outreach tab by setting Status (column I) to a "Send ..." value. Per rules.md 2, that is the user's yes for that one row only. Column H (Action) shows the step; Claude moves it along:

| Action (H) | Status (I) | Meaning |
|---|---|---|
| Connection request | Awaiting approval | drafted, note in L |
| Connection request | Send connection request | the user's yes: send it |
| Request sent | Sent | waiting for them to accept |
| Send DM | Awaiting approval | they accepted, DM in M |
| Send DM | Send DM | the user's yes: send it |
| DM sent | Sent | done (Email sent the same way via "Send email") |

1. `get_values` "Outreach!A1:N". Work = rows with Status "Send connection request" / "Send DM" / "Send email", plus Jobs rows with Status "Approved" (`get_values` "Jobs!N1:O", step 6), plus an acceptance check if any row has Action "Request sent" and state `last_accept_check` is 4h+ old. **No work: end at once** with one line, no browser, no band call.
2. State: `~/.claude/job-hunt/state/outreach.json` (shape in `referral-outreach.md`). Match rows to people by profile URL (column G). Rules.md 0 still applies: skip and flag anyone at the current employer.
3. Caps first: the shared connection cap reached (`quota.linkedin_invites_daily` today or `quota.linkedin_invites_weekly` this week, rules.md 5) means leave "Send connection request" rows as they are and say so in J.
4. Per row, one at a time, in Claude in Chrome (rules.md 1, 5, 8, 9):
   - **Send connection request**: open G, Connect (maybe under "More"), Add a note, paste L exactly (under 200 chars, else flag the row), send. Then H "Request sent", I "Sent". Already 1st-degree: H "Send DM", I "Awaiting approval". Already pending: H "Request sent", I "Sent".
   - **Send DM**: must be 1st-degree, else J "not connected yet", leave it. Message, paste M exactly, attach the PDF named in K from `<resume_dir>/<date>/` with `file_upload`, confirm it shows, send. Then H "DM sent", I "Sent".
   - **Send email**: only if N's address came from the person's own LinkedIn contact info (state `email`) or, for recruiter-email rows (Notes start "Recruiter email"), from SignalHire/Apollo (state in `~/.claude/job-hunt/state/recruiter-email.json`, matched by profile URL). Open that Gmail draft (state `gmail_draft_id`) in Gmail (Chrome), update it to N's text if the user edited it, attach the PDF named in K with `file_upload`, confirm it shows, send. Then H "Email sent", I "Sent" (and that person's state status "sent").
   - **Acceptance check**: open G for each "Request sent" row; 1st-degree now means H "Send DM", I "Awaiting approval". Set `last_accept_check`.
   - Any LinkedIn warning, limit notice or CAPTCHA: stop everything, leave remaining rows untouched, report.
5. After each confirmed step, `update_values` Outreach!H<row>:I<row>, add a dated note in J, update state (status, invited_at / messaged_at, `invites[today] += 1` for connections). A failed row keeps its "Send ..." Status with the reason in J.
6. **Jobs marked Approved** (the user's yes, rules.md 2). `get_values` "Jobs!A1:O"; work = rows with Status (O) "Approved", plus "Weekly limit" rows whose Source's date in state `weekly_limit_until` (state/global-search.json) is today or earlier; skip "Weekly limit" rows before that date without opening the browser (count only the due ones in step 1's "no work" check). Read `references/platforms.md`, `data/answer-bank.md` and `references/resume-tailoring.md` only if there are any. Per row, one at a time: if Resume (L) isn't a tailored PDF path, build one first and write its path to L (resume-tailoring.md, "Every application uses its tailored resume"); attach it on every site that allows an upload. Then by Source (N):
   - **Naukri / LinkedIn / Wellfound / YC Work at a Startup**: open the Job link (M) and apply as platforms.md says, forms from answer-bank.md (Wellfound/YC: write the short note per answer-bank.md, last item). LinkedIn counts toward its daily cap (`quota.linkedin_apply_daily`); at the cap leave the row Approved and say so in Cons. YC allows 5 applications a week: before clicking Send, override `window.alert` / `window.confirm` in the page with `javascript_tool` to record the text (a native alert freezes the tab and the run). If it says the weekly limit is reached, set that row and every other open YC row to "Weekly limit", set `weekly_limit_until["YC Work at a Startup"]` to 7 days after today, add "retry from <date>" to Cons, and stop YC for this run.
   - **Career page / Indeed / country portals** (platforms.md "Country portals"): where the portal applies in-site and the user is signed in (StepStone Schnellbewerbung, Landing.jobs), apply there; otherwise apply on the company form only when it needs no account or sign-in (Greenhouse, Lever, Ashby, SmartRecruiters forms usually don't): fill from answer-bank.md and attach the row's tailored resume PDF (Resume column L) with `file_upload`. A sign-in or account wall (Workday, Google, etc.): set "Apply on site".
   - A question the answer bank doesn't cover: set "Needs your answer" and add "Q: <question>" to Cons. Current employer or excluded company (rules.md 0): set "Not eligible".
   - Applied and confirmed: set "Applied" and add 1 to `applied[today]` in `~/.claude/job-hunt/state/global-search.json` (and `linkedin_applied` for LinkedIn).
   Use `update_values` on "Jobs!O<row>" (find the row by Company + Role + Job link; rows move after sorts).
7. Report: sent, newly accepted, jobs applied / needing the user's answer / apply on site, skipped and why, invites today / this week.
