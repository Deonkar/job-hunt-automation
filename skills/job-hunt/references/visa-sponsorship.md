# Visa sponsorship check

A JD that says nothing about visas is **not** a reason to drop an abroad role. Before any routine marks an abroad job Not eligible for location, or calls it tier 2, check the company. Only these end a role on location:
- the JD itself says no sponsorship, "must already have the right to work", citizens/residents only, or a security clearance; or
- the check below finds the company can't sponsor (e.g. not on the UK or NL sponsor register).

## Cache first
`~/.claude/job-hunt/data/sponsors.json` = `{"<Company>|<country>": {"verdict": "yes|likely|unknown|no", "evidence": "<one line>", "source": "<url>", "checked": "YYYY-MM-DD"}}`. Reuse an entry under 90 days old; otherwise check and write it back.

## How to check (stop at the first strong evidence; 2-4 searches per company is enough)
1. **Official registers** (strongest):
   - UK: Home Office "Register of licensed sponsors: workers" (gov.uk, CSV). On it (Skilled Worker route) = yes; not on it = no.
   - Netherlands: IND "Public register recognised sponsors" (ind.nl), labour / highly skilled migrant. On it = yes; not on it = no (they can't use the highly skilled migrant route).
   - US: H-1B / LCA filings in the last 2 years (USCIS H-1B Employer Data Hub, myvisajobs.com, h1bdata.info), for roles in the user's field. Several filings = yes.
   - Ireland: DETE "employment permits issued to companies" statistics (enterprise.gov.ie). Listed = yes.
   - Canada: positive LMIA employer lists (open.canada.ca) or Global Talent Stream mentions = yes.
2. **Countries where any employer can hire a skilled foreigner** (Germany EU Blue Card, Belgium single permit, Singapore Employment Pass, UAE, Australia, Japan): no register exists, so look for intent, not a licence. Default **likely** for a full-time, mid-pay skilled role at an established company (Germany: salary must clear the Blue Card threshold, so not for internships or low-paid roles); **unknown** for tiny startups with no evidence.
3. **Evidence from the company**: careers page or FAQ ("we sponsor visas", "relocation package", "visa support"), other postings from the same company that mention sponsorship, Glassdoor / Reddit / Blind posts about visas or relocation.
4. **People they have moved**: LinkedIn people search for `<company> <office city>` whose earlier roles were in the user's home country and who joined in the last 3 years. One or more = **yes** (they have done it for someone).

## Use the verdict
- **yes / likely**: tier 1. Pros gets "Sponsors: <evidence>" (e.g. "Sponsors: on UK sponsor register", "Sponsors: 3 people moved from <home country> in 2025"). Pass the same line to Jev as `sponsorship` in the job JSON so it doesn't flag location.
- **unknown**: keep the job (not Not eligible). Cons gets "Sponsorship unverified"; tier 1 only if the company is large and established.
- **no**: Not eligible, with the reason and source in Cons (e.g. "Not on UK sponsor register (checked 2026-10-21)").
