# Candidate: {{full_name}} ({{pronouns_or_blank}})

<!-- Template. `workflows/setup.md` copies this to ~/.claude/job-hunt/data/candidate.md and fills it
     only from the user's resume and their own answers. Never commit the filled copy. -->

- **Now:** {{current_title}} at {{current_company}} ({{one_line_company_description}}), {{city}}, since {{start_month_year}}. {{awards_or_recognition}}
- **Experience:** {{full_time_years_months}} full-time (as of {{date}}) + {{internship_months}} of internships: {{internships_one_line_each}}.
- **Education:** {{degree}}, {{school}}, {{years}}, {{grade}}.
- **Languages spoken:** {{languages_with_levels}}.

## Proof points (pick the 1-2 that match a JD)
<!-- 3-6 lines, each a real result with its number, copied from the resume. -->
- {{proof_point_1}}
- {{proof_point_2}}

## Stack
{{stack_one_line}}. Full list: `data/profile.json`.

## Location preference
- **Tier 1**: {{tier_1_definition}}  <!-- e.g. "roles abroad with visa sponsorship, and remote roles at foreign companies" or "remote roles anywhere" -->
- **Tier 2**: {{tier_2_definition}}  <!-- e.g. "roles in {{home_country}}" -->
- Shortlists, applications and referral picks go tier 1 first, then by score. Score itself stays honest shortlist odds; never inflate it for tier.

## Source priority
- **Primary**: {{primary_sources}}  <!-- default: company career pages and the country portals -->
- **Secondary**: {{secondary_sources}}, capped at {{secondary_daily_cap}} applications a day (`secondary_applied[today]` in `state/global-search.json`). Rows the user sets to Approved in the sheet are their yes and aren't held back by this cap.
- Every shortlist, referral pick and recruiter-email pick orders jobs: tier 1 primary, tier 1 secondary, tier 2 primary, tier 2 secondary; then score within each.

## Best-fit roles (in order)
1. {{target_role_1}}
2. {{target_role_2}}
3. {{target_role_3}}
Drop: {{drop_list}}  <!-- e.g. "senior/staff/lead/manager, internships, roles needing 5+ years, contract roles" -->

## Never
- Current employer: {{current_company}} (and its brands / domains: {{employer_aliases}}). See rules.md 0.
- Other excluded companies: {{excluded_companies_or_none}}.
- Excluded countries: {{excluded_countries_or_none}}.
