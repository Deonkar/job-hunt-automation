# Resume tailoring

Everything is built from the user's master resume by `scripts/build_resume.py` (see the project CLAUDE.md). It clones the master's formatting and refuses invented content: bullets must come from `data/bullets.json`, skill lines must be permutations of the master's. One page always.

## Layers
1. **Variant** (`variants/*.json`): one per target archetype in `profile.targets` (written at setup). Sets headline, summary, skill-line order, which bullets and in what order.
2. **JD patch** (from the `jd-matcher` agent): overrides on top of the variant, using only allowed keys: `skills_order`, `skills_items` (re-order items inside a line, same items), `experience` (per role key, the bullet ids from bullets.json in order, e.g. `{"acme": ["pay", "lat.short"]}`), `projects` (same shape), `projects_order`, `internships`. Write the variant JSON with these keys replaced to `out/applications/<today>/patches/<file-stem>.json` and build from that.
3. **Country** (`countries/*.json`, via `--country`): region US us, UK uk, DE de, NL nl, AU au (add more as `countries/<code>.json`); home country / Remote / other none. Page size, spelling, money and wording swaps (`replace`), work-permit line, CEFR languages, dates.

## Build
```
PYTHONUTF8=1 py -3 scripts/build_resume.py <patch.json> "<OUT>/<First>_<Last>_<Company>_<short-role>.docx" [--country countries/<code>.json]
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/to_pdf.ps1 <docx> [<docx> ...]   # Windows + Word
soffice --headless --convert-to pdf --outdir <OUT> <docx>                            # LibreOffice (macOS / Linux)
```
Every PDF must be 1 page (2 if the user chose that at setup; Word's count or `pdfinfo`); if not, drop JD bullet additions back to the variant's list, then drop the country preset, and say so.

## Where files go (OUT)
OUT = `<resume_dir>/<today>` (create it). Every tailored resume goes there, docx and PDF; the sheet's Resume column gets the PDF's absolute path. Base variant and country resumes live in `<resume_dir>/base/`; rebuild any of them into that folder too. `data/master.docx` stays in the project (the build reads it).

## Every application uses its tailored resume
Before applying to any job (global-search step 5, sheet-actions step 6), the job needs its tailored PDF in OUT. If the row's Resume column has none (global-search jobs, "Profile resume on ..."), build it now: hand the JD text to `jd-matcher` for that one job, write the patch, build + render as above (pages=1). Then attach it:
- **LinkedIn Easy Apply**: at the resume step, "Upload resume", `file_upload` the PDF, select it, confirm its file name is the one ticked before Next.
- **Company forms (Career page / Indeed / Apply on site)**: `file_upload` it in the resume field.
- **Naukri, Wellfound, YC Work at a Startup**: if the apply form offers a resume upload or "change resume", use it. If the site only sends the profile resume, apply with that; never swap the profile resume to do it (that's a profile edit, rules.md 2).
Sheet after applying: Resume = the PDF path; Resume changes = what changed, plus "(not attached: <site> sends the profile resume)" when it couldn't be uploaded.

## Sheet columns this fills
- **Resume changes:** one line, concrete, e.g. "Enterprise sales variant (headline + summary); skills: CRM tools first; bullets: quota attainment, new-logo deals (short); UK format (A4, British spelling, right-to-work line)".
- **Skills to learn:** JD requirements absent from `data/profile.json` skills (and `skills_beyond_resume`), e.g. "Terraform, Django" or "Gong, MEDDIC". Never added to the resume.
