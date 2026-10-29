# Answer bank ({{full_name}}, last updated {{date}})

<!-- Template. `workflows/setup.md` copies this to ~/.claude/job-hunt/data/answer-bank.md and fills it
     from the user's answers to `references/questionnaire.md`. Never commit the filled copy.
     "Prefer not to say" is a valid answer everywhere in Self-identification. -->

Fill forms only from here or from what the user says in chat that day. Anything not covered: stop that job, set it "Needs your answer" with "Q: <question>" in Cons, and ask. Never invent an answer. When the user answers a new question, add it here (with the date) so it is never asked twice.

## Contact (forms only, never on public pages)
- **Email:** {{email}}  **Phone:** {{phone_with_country_code}}  **WhatsApp opt-in:** {{yes_no}}
- **Current location (city, country):** {{city_country}}. "If located in the US, city and state": {{us_city_state_or_not_in_us}}.
- **Links:** LinkedIn {{linkedin}}, GitHub {{github}}, portfolio {{portfolio}}.

## Experience
- **Current employer / title:** {{current_company}}, {{current_title}}, since {{start}}.
- **Total experience:** {{full_time}} full-time + {{internships}} internships. "Years of experience" = {{years_rule}}  <!-- e.g. full-time figure unless the form says internships count -->
- **Years with a technology:** only stacks on the resume, at most the full-time years each: {{per_tech_years}}. Anything else: 0 or ask.
- **"Do you possess N years of experience in X?" (yes/no):** answer honestly from the line above. If the honest answer is No, still answer No and flag "likely auto-reject" in Cons.
- **Years in a domain (payments, data, ML...):** {{domain_years}}.
- **DSA / coding self-rating (1-10):** {{dsa_rating}}. Other self-ratings: {{other_ratings_or_ask}}.
- **Reason for change (one line):** {{reason_for_change}}.
- **Titles for background checks:** use the titles on offer letters: {{exact_titles}}.

## Notice and joining
- **Notice period:** {{notice_days}} days, {{negotiable_or_not}}. Dropdowns: "{{notice_dropdown}}". Serving notice: {{serving_notice}} (last working day {{lwd_or_na}}).
- **Earliest start:** {{earliest_start}}. Immediate-joiner roles: {{immediate_joiner_policy}}.
- **Interview availability:** {{days_times_timezone}}. In-person interview in another city: {{in_person_policy}}.

## Compensation ({{currency}})
- **Current:** total {{current_total}} ({{current_fixed}} fixed + {{current_variable}} variable{{plus_stock_or_bonus}}). Fixed only: {{current_fixed}}. Disclose current pay: {{disclose_policy}}.
- **Expected (home country):** floor {{floor}}, never below it. Per role:
  - {{tier_a_companies}}: {{range_a}}
  - {{tier_b_companies}}: {{range_b}}
  - {{tier_c_companies}}: {{range_c}}
  - Single-number field: the chosen figure; range field: a band inside the range for that tier.
- **Expected outside home country:** {{abroad_salary_answer}}  <!-- e.g. "Negotiable, in line with the market for the role"; midpoint of a posted range if a number is required -->
- **Contract / hourly rate:** {{hourly_or_not_open_to_contract}}.
- **Pay below the floor:** mark the job Not eligible ("pay below floor").

## Work mode and location
- **Work mode:** {{remote_hybrid_onsite}}. Office 5 days a week: {{five_day_office}}. Plan to work remotely: {{remote_answer}}.
- **Shifts:** US / UK / AU or rotational shifts: {{shift_answer}}. Night shifts: {{night_shift}}. Travel: up to {{travel_percent}}%.
- **Relocation (home country):** {{relocate_home}}.
- **Relocation (abroad):** {{relocate_abroad_countries}}; never {{excluded_countries}}.
- **Visa sponsorship needed:** {{sponsorship_by_country}}. **Currently authorized to work in:** {{authorized_countries}}. Citizenship(s): {{citizenships}}.
- **Located in a specific state/province (e.g. "Are you located in Quebec?"):** {{answer_from_location}}.

## Education
- **Highest qualification:** {{degree}}, {{school}}, {{grad_year}}, {{grade}}.
- **School marks if asked (class 10 / 12, A-levels...):** {{school_marks_or_ask}}.
- **Transcripts and certificates:** files at {{transcripts_path_or_ask}}.

## Self-identification (EEO / diversity; every answer may be "Prefer not to say")
- Gender: {{gender}}; pronouns: {{pronouns}}; race / ethnicity: {{race}}; Hispanic or Latino: {{hispanic}}; sexual orientation: {{orientation}}; transgender: {{trans}}; disability: {{disability}}; protected veteran: {{veteran}}.
- Date of birth / age: {{dob_or_not_shared}}. Nationality: {{nationality}}. Marital status: {{marital_or_not_shared}}.

## Legal and consent
- **Relatives at the company:** {{relatives}}. **Related to a government official:** {{gov_relation}}. **Ever employed by a government or public body:** {{gov_employment}}.
- **Non-compete / NDA limits:** {{non_compete}}. **Background check consent:** {{background_check}}.
- **Privacy notices, terms, arbitration agreements on application forms:** {{consent_policy}}  <!-- default: "ask me each time" (rules.md 2) -->
- **"How did you hear about this job?":** the Source (e.g. "Company website", "LinkedIn"), or "Referral: <name>" when a referral was given.
- **Previously applied / worked here:** check the Jobs sheet; otherwise "No".

## Approved texts (reuse word for word; add new ones as the user approves them)
- **Why this company / role notes (Wellfound, YC, cover notes):** 2-3 sentences, specific to the company, one proof point from `data/candidate.md`, no claims beyond it. Show each note with the shortlist; it is part of the application the user approves.
- **Most impactful thing built:** {{impact_story}}
- **How you use AI tools today:** {{ai_tools_answer}}
- **What motivates you (200 chars):** {{motivation}}
- **A system you shipped and how you knew it worked:** {{shipped_and_measured}}
- **Project with non-engineering stakeholders:** {{stakeholder_story}}
- **A failure and what changed after:** {{failure_story}}
- **Cover letter:** {{cover_letter_policy}}  <!-- e.g. "only when required; 150 words from candidate.md" -->
