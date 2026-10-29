# Setup questionnaire

The questions `workflows/setup.md` asks, in rounds. Every one comes from a real application form, recruiter screen or routine decision that otherwise stops a run with "Needs your answer". Works for any field: software, data, design, sales, HR / recruiting, marketing, finance, operations, customer success, teaching, healthcare and more. Question 1.7 sets the field; adapt the examples in every later round to it and skip questions marked (tech) for non-tech users. Ask one round at a time (use AskUserQuestion for the choice questions, plain chat for free text), show what you already know from the resume as the default, and let the user skip anything: a skipped question is asked again the first time a form needs it. "Prefer not to say" is always allowed in round 9.

Column "Goes to" says where the answer is stored (all under `~/.claude/job-hunt/data/`): **P** `profile.json`, **C** `candidate.md`, **A** `answer-bank.md`, **G** `config.json`, **E** `../.env`.

## Round 1: resume and identity
| # | Question | Goes to |
|---|---|---|
| 1.1 | Path to your latest resume (PDF or DOCX), or paste it. Is it up to date? | P, bullets.json |
| 1.2 | Full name as it should appear on applications; preferred first name for messages | P, A |
| 1.3 | Email and phone (with country code) for applications. OK to opt in to WhatsApp updates from employers? | P, A |
| 1.4 | City and country you live in now | P (location, home_country), A |
| 1.5 | LinkedIn, plus what your field uses: GitHub (tech), portfolio / Behance / Dribbble (design), publications, certifications page | P (links), A |
| 1.6 | Pronouns (optional) | C, A |
| 1.7 | Your field and function (e.g. software engineering, sales, HR / talent acquisition, marketing, finance, operations, design). Switching fields? From what to what? | P (field), C |

## Round 2: current job
| # | Question | Goes to |
|---|---|---|
| 2.1 | Current company, exact title (as on your offer letter), start month, team / product | P, C, A |
| 2.2 | Other names / brands / domains of your employer (so the routines never apply there or contact colleagues) | G (employer_aliases), C |
| 2.3 | Awards or recognition at this job, with dates | P, C |
| 2.4 | Notice period in days; negotiable? Currently serving notice (last working day)? Buy-out possible? | A |
| 2.5 | One honest line for "reason for change" | A |
| 2.6 | Are you employed right now (if not, since when and why: gap, layoff, study)? | A |

## Round 3: previous jobs, internships, education
| # | Question | Goes to |
|---|---|---|
| 3.1 | Each earlier job and internship: company, title as on the offer letter / certificate, start and end month, remote or on-site. (Background checks compare against those letters.) | P, bullets.json |
| 3.2 | Does your experience count internships, or full-time only? What do you answer for "total years of experience"? | A |
| 3.3 | Highest degree, school, years, GPA / percentage / class | P, A |
| 3.4 | School marks if forms ask (class 10 / 12, A-levels, high school) and where your transcripts and certificates PDFs are | A |
| 3.5 | Projects, certifications or portfolio pieces you want on the resume: name, tools, link, one result each (optional; most non-tech resumes skip this) | P (projects), bullets.json |
| 3.7 | Certifications and licences (e.g. PMP, SHRM, CFA, AWS, Salesforce Admin) with year | P (skills), A |
| 3.6 | Languages you speak, with level (native / C1 / B2...) | P (spoken_languages), C |

## Round 4: compensation
| # | Question | Goes to |
|---|---|---|
| 4.1 | Currency you are paid in | A |
| 4.2 | Current total pay, split: fixed, variable / bonus, stock. OK to disclose it on forms? | A |
| 4.3 | Expected pay: your floor (never go below), and a range per company type (e.g. service / early startup, funded product / fintech, big tech) | A |
| 4.4 | What to answer for expected salary abroad (free text, or a number per country) | A |
| 4.5 | Open to contract / freelance roles? Hourly or day rate? | A, P (search) |
| 4.6 | Jobs that list pay below your floor: skip them, or still show them? | A |

## Round 5: what you want
| # | Question | Goes to |
|---|---|---|
| 5.1 | Target roles in order (titles), and the level (junior, mid, senior, staff, manager) | P (targets), C |
| 5.2 | Words a job title must contain (e.g. "account executive", "sales" / "recruiter", "talent acquisition" / "engineer", "developer"), words that make it a strong match, and words to always skip (senior, intern, director...) | P (search.include_title_words, strong_title_words, exclude_title_words) |
| 5.3 | Years of full-time experience to compare JDs against | P (search.years) |
| 5.4 | Industries / domains you want and ones to avoid; company size and stage | C |
| 5.5 | Dream companies to watch; companies never to apply to (besides your employer) | G (excluded_companies), companies list |
| 5.6 | Employment type: full-time only, or also contract / internship? | C, P (search) |
| 5.7 | Search keywords for job boards (default: your target titles) | P (search.keywords) |

## Round 6: location, work authorization, work mode
| # | Question | Goes to |
|---|---|---|
| 6.1 | Work mode: remote, hybrid, on-site. OK with 5 days a week in office? | A |
| 6.2 | Relocate within your country? Which cities, or anywhere? | A |
| 6.3 | Relocate abroad? Which countries; any you would never go to? | A, P (search.regions), G |
| 6.4 | Citizenship(s); countries where you can already work without sponsorship | A |
| 6.5 | Do you need visa sponsorship (per country)? | A, C (tier 1 / tier 2) |
| 6.6 | Shifts: OK with US / UK / AU hours, rotational or night shifts? Travel up to what %? | A |
| 6.7 | Available for in-person interviews in other cities? Interview days and hours, time zone | A, G (timezone) |
| 6.8 | Earliest start date; can you join immediately if a role needs it? | A |

## Round 7: skills, honestly
| # | Question | Goes to |
|---|---|---|
| 7.1 | Confirm the skills list parsed from your resume, grouped as on the resume (tools, methods, domains: e.g. Salesforce, HubSpot, Excel, Workday, SQL, Figma, Go). Remove anything you could not defend in an interview | P (skills) |
| 7.2 | Years with each main tool or technology (at most your full-time years) | A |
| 7.3 | Years in each domain or segment (B2B SaaS, enterprise sales, campus hiring, payments, healthcare...) | A |
| 7.4 | Numbers and self-ratings forms ask in your field: sales quota attainment %, average deal size, pipeline; hires closed per quarter, time to hire; campaign results; DSA / problem solving 1-10 (tech); English / communication level | A |
| 7.5 | Skills you have used but are not on the resume (and why) | P (skills_beyond_resume) |
| 7.6 | Other names for your skills that JDs use (golang for Go, SFDC for Salesforce, TA for talent acquisition...) | P (keyword_aliases) |

## Round 8: stories forms ask for (draft from the resume, the user edits and approves)
| # | Question | Goes to |
|---|---|---|
| 8.1 | Your 3-6 strongest results, each with a number (these become proof points) | C |
| 8.2 | The most impactful thing you built and your part in it | A |
| 8.3 | A result you delivered and how you measured it (revenue, hires, conversion, latency, savings) | A |
| 8.4 | A project with people outside your team (other departments, clients) and its impact | A |
| 8.5 | How you use AI tools in your work today | A |
| 8.6 | What motivates you (200 characters); a failure and what you changed | A |
| 8.7 | Cover letters: write one when optional, only when required, or never? | A |

## Round 9: self-identification and legal (all optional; "Prefer not to say" is fine)
| # | Question | Goes to |
|---|---|---|
| 9.1 | Gender; transgender; sexual orientation | A |
| 9.2 | Race / ethnicity; Hispanic or Latino | A |
| 9.3 | Disability; protected veteran status | A |
| 9.4 | Date of birth / age, nationality, marital status (only some countries' forms ask; leave blank to be asked each time) | A |
| 9.5 | Relatives at a company you apply to? Related to a government official? Ever employed by a government or public body? | A |
| 9.6 | Non-compete or NDA limits; OK with background checks? | A |
| 9.7 | Privacy notices, terms, arbitration agreements on forms: ask you each time (default), or accept standard privacy notices only? | A |

## Round 10: tools, accounts and keys
| # | Question | Goes to |
|---|---|---|
| 10.1 | Which job sites to use: LinkedIn, Indeed, Naukri (India), Wellfound and YC Work at a Startup (startups, mostly tech), country portals (pick countries). Are you signed in to them in Chrome? | G (platforms) |
| 10.2 | Google account for the tracker: are the Google Sheets, Drive and Gmail connectors connected? Create the job sheet in your Drive now? | G (sheet ids) |
| 10.3 | Firecrawl API key (optional; reads career pages and job descriptions without opening Chrome tabs). Get one at firecrawl.dev | E (FIRECRAWL_API_KEY) |
| 10.4 | TypeSafe API key for the optional "Jev: apply?" column (skip to leave it off) | E (TYPESAFE_API_KEY) |
| 10.5 | SignalHire or Apollo Chrome extension for recruiter work emails (optional) | G (recruiter_email_tools) |
| 10.6 | Folder for tailored resumes (default `~/Desktop/job_resumes`); Word or LibreOffice for PDFs | G (resume_dir, pdf) |

## Round 11: pace and permissions
| # | Question | Goes to |
|---|---|---|
| 11.1 | Applications a day (default 10-15), and the cap for job-board (secondary) applications (default 5) | G (quota) |
| 11.2 | LinkedIn limits (defaults: 5 Easy Apply a day, 15 connection requests a day, 100 a week; never higher) | G (quota) |
| 11.3 | Which routines to schedule, and at what local times (defaults in `SKILL.md`) | G (routines) |
| 11.4 | Standing approvals: plain no-note connection requests to engineers and recruiters at watchlist companies? A small daily truthful Naukri profile edit? (Default: no; everything else always asks.) | G (standing_yes) |
| 11.5 | Writing style for messages: sign-off name, plain punctuation (no em dashes or arrows) on? | G |

## Round 12: your public profiles
| # | Question | Goes to |
|---|---|---|
| 12.1 | Which profiles to optimize now: LinkedIn, Naukri, Indeed, Wellfound, YC Work at a Startup (each is reviewed section by section; nothing is saved without your yes) | runs `workflows/profile-refresh.md` |
| 12.2 | LinkedIn: OK to install the free `linkedin-skills` plugin (sergebulaev/linkedin-skills, MIT) for the full profile audit? Open to Work on: recruiters only, or public? | G |
| 12.3 | Naukri: two truthful resume headlines to rotate, and do you want the small daily profile edit that keeps you near the top of recruiter searches (standing yes)? | G (naukri_headlines, standing_yes) |
