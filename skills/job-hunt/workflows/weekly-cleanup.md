# Workflow: weekly rejection check and cleanup (Sundays)

Read: `references/rules.md`, `references/sheet.md`, `references/progress-band.md`.

1. **Band**: `cleanup-<today>`, links Jobs sheet, Resumes folder.
2. **Load applications**: Sheets `get_values` "Jobs!A:O". Candidates: Status Applied, Ready to apply or Apply on site, Date found 5+ days ago.
3. **Find outcomes** (data-scan), cheapest first:
   - Gmail connector `search_threads` over the last 60 days: `("unfortunately" OR "not moving forward" OR "other candidates" OR "not be progressing" OR "regret to inform" OR "position has been filled") newer_than:60d`, then match each thread to a candidate row by company name (sender domain or body) and role. Read only the threads that match.
   - LinkedIn `https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED` and, when Naukri is on, `https://www.naukri.com/mnjuser/applies`: read statuses ("No longer accepting applications", "Rejected", "Not selected") for candidates from those sources.
   Treat only explicit rejection or a closed role after the user applied as rejected. Anything 30+ days with no reply is "No response" (no cleanup).
4. **Propose**: one table: company, role, source, evidence (email subject + date, or the status text), proposed status (Rejected / No response), and the resume file to set aside (Rejected only, and only tailored PDFs in `<resume_dir>/<date>/`; never anything in `<resume_dir>/base/`). Ask "Apply these updates?".
5. **After the user's yes**: Sheets `update_values` the Status cell of each row (sheet.md, How). For each Rejected row's tailored PDF in `<resume_dir>`: move it (and its docx) to `<resume_dir>/_rejected/` and update the row's Resume path. Never delete files or empty trash.
6. **Report**: rows checked, rejected, no response, resumes moved (names), anything unclear left for the user.
