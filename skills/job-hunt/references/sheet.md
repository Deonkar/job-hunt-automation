# job_sheet (Google Sheets connector)

Spreadsheet id `config.sheet_id`. Use the Sheets connector (ToolSearch "google sheets append values"); never paste through Chrome or the clipboard.

## Tabs and columns
**Jobs** (gid 0), 15 columns A-O, hidden helper P, then Q:
Date found | Company | Role | Location | Region | Posted | Score | Pros | Cons | Resume changes | Skills to learn (in JD, not on resume) | Resume | Job link | Source | Status | (P, hidden) Sort group | Jev: apply?
- Sort group (P): formula `=IF(REGEXMATCH(INDIRECT("O"&ROW()),"^(Applied|Not eligible|Skipped|Wrong search|Not approved|Rejected|No response)$"),1,0)`, 1 = done (already applied, or not going to apply), sinks to the bottom. Interview stays on top: it needs the user's action. Never write data there; the sort step below fills it.
- Jev: apply? (Q, optional, on when `config.jev` and a TypeSafe key in `.env`): Jev's yes/no on whether the user should apply, from `scripts/jev_verdict.py` (project folder). Before appending any Jobs rows, write those jobs (company, role, location, region, posted, source, pros, cons, skills_to_learn, link, `sponsorship` (the visa-sponsorship.md evidence line, for abroad roles), and `jd` text when the run read it) as a JSON list to `out/jev/<today>-<HHMM>.json`, run `PYTHONUTF8=1 py -3 scripts/jev_verdict.py <that file> --out <that file minus .json>-out.json`, and put each job's `jev` string in Q, as is: "Yes (0.82)", "No (0.18): experience gap, location", or "Jev error: ..." (never retry or block the run on it; a missing key exits with a message: write "Jev: no key" in Q and say so in the report). It's advice for the user only: it never changes Score, Status, shortlists or what gets applied.
- Score: 0-100 shortlist odds. Pros/Cons: two short items each, honest.
- Resume changes: what the tailored resume changed vs the master (see resume-tailoring.md); "Profile resume on <site>" when the site uses the user's uploaded resume.
- Skills to learn: JD skills/tools the user doesn't have, comma-separated; empty if none.
- Resume: absolute path of the tailored PDF in `<resume_dir>/<date>/` (resume-tailoring.md); "Profile resume on <site>" only until it is built at apply time.
- Source: Career page / Naukri / LinkedIn / Indeed / Wellfound / YC Work at a Startup, or a country portal name as `platforms.md` "Country portals" lists it (e.g. StepStone, IamExpat Jobs, Relocate.me).
- Status (dropdown, strict, only these values): Ready to apply / Needs your answer / Approved / Weekly limit / Apply on site / Applied / Skipped / Wrong search / Not approved / Not eligible / Next day / Interview / Rejected / No response. The user sets Approved, Applied, Skipped, Wrong search themselves; never overwrite those except to move an Approved row on after acting on it. Colours (conditional formats on O, legend in the O1 note): the user's move = warm (Needs your answer amber, Apply on site orange, Ready to apply blue, all bold); Approved teal bold; Weekly limit slate blue bold; Applied light green; Interview dark green; Next day purple; No response grey; Rejected red; Not approved / Not eligible / Skipped / Wrong search grey italic. Use only dropdown values so the colours apply.
  - Not approved = it was offered in a shortlist and the user didn't pick it (the user can switch it to Approved later). Not eligible = the routine ruled it out (years, contract, location, excluded company); put the reason in Cons. Location only per `visa-sponsorship.md` (a JD silent on visas is not enough). Never use Not approved for an eligibility drop.
  - Approved = the user's yes to apply (rules.md 2); `workflows/sheet-actions.md` applies and then sets Applied / Needs your answer / Apply on site.
  - Weekly limit = still the user's yes, but the site's weekly application cap is full (YC Work at a Startup: 5 a week; it shows a browser alert "You've reached your limit of 5 applications per week" that freezes the page). The reset date is in state `weekly_limit_until[<Source>]` in `state/global-search.json` and in Cons ("retry from <date>"). Routines skip these rows until that date, then sheet-actions applies them like Approved, sending the "APPROVED NOTE (send exactly)" text stored in Resume changes (J) word for word.

**Outreach**, 14 columns A-N, one row per person: Date | Person | Title | Company | Job | Job link | Profile | Action (Connection request / DM / Email draft) | Status | Notes | Resume (attached to DM) | Connection note | DM (sent after they accept) | Email
- Action (H, written by Claude, shows where the person is): Connection request > Request sent > Send DM (they accepted) > DM sent > Email sent; or Replied / Stale.
- Status (I, the user's dropdown, strict): Awaiting approval / Send connection request / Send DM / Send email / Sent / Replied / Stale / Skip. The three "Send ..." values are the user's approval triggers (yellow), handled by `workflows/sheet-actions.md`. Action "Send DM" is also yellow: it means pick "Send DM" in Status.
- Fill K-N when the row is created: the resume PDF file name, the exact connection note, the exact DM, and the exact email (subject line first) or why there is none. These cells are the text that gets sent; if the user edits them, send the user's edited text.

**Companies**: the watchlist (Company, Segment, Region, Careers page, How it's checked, Feed, Open roles, Notes).

## How
- Append: `append_values` with range "Jobs!A1" (or "Outreach!A1"), one array per row in column order; Jobs rows have 17 values: A-O, "" for P, the Jev cell for Q. Then `get_values` on the last rows to confirm.
- Keep Jobs sorted: open rows on top, done rows at the bottom: Applied / Not eligible / Skipped / Wrong search / Not approved / Rejected / No response; within each, newest first then highest score. Do it after **every** Jobs write (append or Status change), once at the end of the batch of writes. Two separate `update_spreadsheet` calls, in this order (one combined call sorts before the formulas calculate and nothing moves):
  1. `repeatCell` on sheetId 0, rows 2 to the last data row (startRowIndex 1, endRowIndex = last row number), column P (15-16), `userEnteredValue.formulaValue` = the Sort group formula above, fields "userEnteredValue". Safe to overwrite every row: the formula reads its own row.
  2. `sortRange` on the same rows, columns A-Q (0-17, so Jev's cell moves with its row), sortSpecs P (15) ASCENDING, A (0) DESCENDING, G (6) DESCENDING.
  Rows move, so find a row by Company + Role + Job link before updating it.
- Rows can move under a running routine if the user sorts or edits mid-run (or adds an optional Apps Script `onEdit` sort), so always re-find a row right before writing it.
- Update a cell (e.g. Status): `get_values` "Jobs!A:O" to find the row (match Company + Role + Job link), then `update_values` on "Jobs!O<row>". Then re-sort (above).
- Strings only for dates and links (the connector parses input like the Sheets UI).
