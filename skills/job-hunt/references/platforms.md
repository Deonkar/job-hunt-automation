# Platforms

Use only the platforms on in `config.platforms`. The user signs in to each in their own Chrome (never sign in for them, rules.md 1). Search terms everywhere = `profile.search.keywords` (their target titles in their field: "account executive", "talent acquisition specialist", "backend engineer"...). Read listings with `get_page_text`; keep each platform's search tab open and reload it (rules.md, tabs).

## Naukri (India; apply in-site)
- Search: `https://www.naukri.com/<query-with-dashes>-jobs?k=<url-encoded query>&experience=<profile.search.years>&jobAge=1` (jobAge=3 if thin).
- Queries: each `profile.search.keywords` term, plus "<main skill> <role>" combinations for the user's top 2-3 skills.
- Apply: the Apply button, confirm "applied". A questionnaire or a company-site redirect stops that job (rules.md 3).
- Profile: `https://www.naukri.com/mnjuser/profile`.

## LinkedIn Easy Apply (max `quota.linkedin_apply_daily`/day, rules.md 5)
- Search: `https://www.linkedin.com/jobs/search/?keywords=<q>&f_AL=true&f_TPR=r10800&f_E=<experience levels>&sortBy=DD&location=<loc>` for each `profile.search.keywords` term. f_E: 1 internship, 2 entry, 3 associate, 4 mid-senior, 5 director, 6 executive; pick the levels around `profile.search.years`.
- loc: the home country (or city) and Remote every run, plus, if the user targets other countries (`profile.search.regions`), two of them rotating by run hour. Abroad: never drop a role just because the JD doesn't mention visas; run the sponsorship check (`visa-sponsorship.md`) first.
- Apply: Easy Apply, fill from the answer bank, review, submit, confirm "Application sent".

## Indeed (connector, apply on site)
- `search_jobs` for the first two `profile.search.keywords` terms with the home country's country_code / location, and location "remote"; keep jobs from the last 1-3 days. Apply links go in the sheet as "Apply on site".

## Wellfound (startups; apply in-site with a note)
- Profile: `https://wellfound.com/profile/edit` (update before applying, see profile-refresh.md).
- Search: `https://wellfound.com/jobs` (results follow the user's saved job preferences: target roles, experience band, locations; set them once in profile-refresh). Startup roles across engineering, product, design, sales, marketing and operations. Read with get_page_text.
- Apply: "Apply" opens a form with a note to the hiring team. Draft a short note per job (answer-bank.md, last item) and show it in the shortlist; submit only after the user's yes.

## YC Work at a Startup (YC companies; apply = message to founders)
- Profile: `https://www.workatastartup.com/` (candidate profile, update before applying). Note: `ycombinator.com/apply` is YC's founder application for starting a company, not a job profile; don't use it for job search.
- Search: `https://www.workatastartup.com/jobs`. **Set the filters on the page before reading; never read the unfiltered list**: the user's role family (engineering, design, product, sales, operations...), Full-time, their experience band, location Remote + the home country, and the visa / work-authorization filter set to roles open without US authorization (e.g. "Will sponsor") if the page has one. Read with get_page_text. If a filter won't set, say which in the report. Public YC board as fallback: `https://www.ycombinator.com/jobs`.
- Ruled-out YC jobs still go in the sheet, so a YC search is visible: up to 5 per run (closest title fits, not in state.seen) as Jobs rows with Status "Not eligible", Source "YC Work at a Startup", the reason in Cons (e.g. "US work authorization only"). Add them to state.seen.
- Report line every run: "YC: filters <set / which failed>, <n> listings, <n> kept, <n> ruled out (<main reason>)".
- Apply: "Apply" sends a short message to the founders. Draft it per job and get the user's yes, like Wellfound.
- Limit: 5 applications a week. Before Send, override `window.alert`/`window.confirm` with `javascript_tool` so the "You've reached your limit of 5 applications per week" alert is captured instead of freezing the tab. Before applying, skip YC entirely while state `weekly_limit_until["YC Work at a Startup"]` (state/global-search.json) is after today; on the alert, set it to 7 days ahead and mark the job "Weekly limit" (sheet.md).

## Company career pages
- Watchlist companies with public job feeds (Greenhouse, Lever, Ashby, SmartRecruiters, Workday, Amazon) are polled by `scripts/scout.py` (no tokens). Those without feeds are browser-only: one open tab each, or Firecrawl when on (see company-scan.md).

## Country portals (`workflows/country-portals.md`, daily 18:30)
Only the portals listed in `config.platforms.country_portals` are used. The user may not be signed in to them: read what is public and log the portal under `login_needed` instead of signing in (rules.md 1). Search terms on every portal: the `profile.search.keywords` terms in order (and the local-language title where the portal is not in English, only if the user speaks that language). Set filters on the page (English-language jobs where offered, last 24h, full-time, not senior); bot checks and cookie banners: decline non-essential cookies, stop on any CAPTCHA (never solve one). Source column = the name in bold.

**Daily** (every run):
- **Relocate.me** `https://relocate.me/international-jobs`: only jobs with relocation and visa support, all countries. Apply goes to the company form.
- **Landing.jobs** `https://landing.jobs/jobs`: Europe, many with relocation (filter "relocation"). Apply in-site with a profile.
- **StepStone** (DE) `https://www.stepstone.de/jobs/software-engineer`: biggest German board. "Schnellbewerbung" applies in-site when signed in; otherwise company form.
- **XING Jobs** (DE) `https://www.xing.com/jobs/search?keywords=software+engineer`.
- **Arbeitsagentur** (DE) `https://www.arbeitsagentur.de/jobsuche/suche?was=Software%20Engineer`: the federal job board; listings link to the employer.
- **Make it in Germany** (DE) `https://www.make-it-in-germany.com/en/working-in-germany/job-listings`: the government board for foreign skilled workers (English).
- **Berlin Startup Jobs** (DE) `https://berlinstartupjobs.com/engineering/`: English-speaking startups.
- **IamExpat Jobs** (NL) `https://www.iamexpat.nl/career/jobs-netherlands`: English-speaking roles in the Netherlands (category IT).
- **Nationale Vacaturebank** (NL) `https://www.nationalevacaturebank.nl/`: search "software engineer", mostly Dutch; keep only English JDs.

**Group A** (even day-of-year):
- **IrishJobs** (IE) `https://www.irishjobs.ie/`.
- **Reed** (UK) `https://www.reed.co.uk/jobs/software-engineer-jobs`.
- **Welcome to the Jungle** (UK/EU, formerly Otta) `https://www.welcometothejungle.com/en/jobs`: has a "visa sponsorship" filter, use it.
- **jobs.ch** (CH) `https://www.jobs.ch/en/`.
- **karriere.at** (AT) `https://www.karriere.at/jobs`.

**Group B** (odd day-of-year):
- **EuroTechJobs** (EU) `https://www.eurotechjobs.com/`.
- **The Hub** (Nordics) `https://thehub.io/jobs`: Nordic startups, English.
- **Just Join IT** (PL) `https://justjoin.it/`: filter remote / relocation.
- **MyCareersFuture** (SG) `https://www.mycareersfuture.gov.sg/`: Singapore's government board (Employment Pass roles).
- **SEEK** (AU) `https://www.seek.com.au/software-engineer-jobs`.
