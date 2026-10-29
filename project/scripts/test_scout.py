import datetime as dt
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import scout  # noqa: E402

TODAY = dt.date(2026, 10, 19)
PROFILE = {
    "skills": {"Languages": ["Go", "Ruby", "TypeScript"], "Data": ["PostgreSQL", "Redis", "Kafka"],
               "AI / ML": ["RAG"]},
    "keyword_aliases": {"Go": ["golang"], "PostgreSQL": ["postgres"]},
}


class TitleTest(unittest.TestCase):
    def test_keeps_engineering_roles_at_his_level(self):
        for t in ["Software Engineer", "SDE II", "Backend Engineer (Payments)", "Full Stack Developer",
                  "AI Engineer", "Software Engineer, New Grad", "Product Engineer", "SDE-1", "Applied AI Engineer"]:
            self.assertTrue(scout.title_ok(t), t)

    def test_drops_senior_and_non_engineering_roles(self):
        for t in ["Senior Software Engineer", "Staff Engineer", "Engineering Manager", "Principal Engineer",
                  "Sales Engineer", "Solutions Engineer", "Software Engineering Intern", "Sr. Backend Engineer",
                  "Lead Developer", "Recruiter", "Data Analyst", "Director of Engineering"]:
            self.assertFalse(scout.title_ok(t), t)


class ProfileFilterTest(unittest.TestCase):
    def test_title_exclusions_come_from_the_profile(self):
        self.assertTrue(scout.title_ok("Senior Backend Engineer", ["intern"]))
        self.assertFalse(scout.title_ok("Backend Engineer Intern", ["intern"]))
        self.assertTrue(scout.title_ok("Staff Engineer", []))

    def test_non_tech_candidate_sets_their_own_title_words(self):
        sales = {"include": ["account executive", "sales", "business development"], "exclude": ["intern", "director"]}
        self.assertTrue(scout.title_ok("Enterprise Account Executive", sales["exclude"], sales["include"]))
        self.assertTrue(scout.title_ok("Sales Manager, EMEA", sales["exclude"], sales["include"]))
        self.assertFalse(scout.title_ok("Software Engineer", sales["exclude"], sales["include"]))
        self.assertFalse(scout.title_ok("Sales Director", sales["exclude"], sales["include"]))

    def test_strong_title_bonus_comes_from_the_profile(self):
        job = {"title": "HR Business Partner", "description": "", "posted": TODAY}
        plain = scout.score(job, PROFILE, TODAY)
        hr = scout.score(job, dict(PROFILE, search={"strong_title_words": ["hr business partner"]}), TODAY)
        self.assertEqual(hr - plain, 10)

    def test_years_penalty_is_relative_to_the_candidate(self):
        job = {"title": "Backend Engineer", "description": "Go, Postgres. 5+ years of experience", "posted": TODAY}
        junior = scout.score(job, PROFILE, TODAY)
        senior = scout.score(job, dict(PROFILE, search={"years": 6}), TODAY)
        self.assertGreater(senior, junior)


class LocationTest(unittest.TestCase):
    def test_target_locations(self):
        for loc, want in [("Bengaluru, India", "IN"), ("Pune", "IN"), ("Remote", "Remote"),
                          ("Berlin, Germany", "DE"), ("Amsterdam", "NL"), ("London, UK", "UK"),
                          ("Sydney, Australia", "AU"), ("Toronto, Canada", "CA"),
                          ("Dublin, Ireland", "IE"), ("Singapore", "SG"), ("Dubai, UAE", "AE"), ("San Francisco, CA", "US"), ("Remote - India", "IN")]:
            self.assertEqual(scout.region_of(loc), want, loc)

    def test_other_locations_are_dropped(self):
        for loc in ["São Paulo, Brazil", "Tokyo, Japan", "Mexico City"]:
            self.assertIsNone(scout.region_of(loc), loc)


class YearsTest(unittest.TestCase):
    def test_reads_minimum_years(self):
        self.assertEqual(scout.min_years("You have 3+ years of experience building APIs"), 3)
        self.assertEqual(scout.min_years("2-4 years of professional experience"), 2)
        self.assertEqual(scout.min_years("at least five years of experience"), 5)
        self.assertIsNone(scout.min_years("We love Go and Postgres"))

    def test_ignores_company_age(self):
        self.assertIsNone(scout.min_years("Founded 10 years ago, we serve customers"))


class PostedTest(unittest.TestCase):
    def test_parses_each_source_format(self):
        self.assertEqual(scout.parse_posted("2026-10-17T09:00:00-04:00", TODAY), dt.date(2026, 10, 17))
        self.assertEqual(scout.parse_posted(1792200000000, TODAY), dt.date(2026, 10, 17))
        self.assertEqual(scout.parse_posted("Posted Today", TODAY), TODAY)
        self.assertEqual(scout.parse_posted("Posted Yesterday", TODAY), dt.date(2026, 10, 18))
        self.assertEqual(scout.parse_posted("Posted 3 Days Ago", TODAY), dt.date(2026, 10, 16))
        self.assertEqual(scout.parse_posted("Posted 30+ Days Ago", TODAY), dt.date(2026, 9, 19))
        self.assertEqual(scout.parse_posted("October 18, 2026", TODAY), dt.date(2026, 10, 18))
        self.assertIsNone(scout.parse_posted(None, TODAY))


class ScoreTest(unittest.TestCase):
    def test_keyword_overlap_uses_aliases_and_word_boundaries(self):
        hits = scout.keyword_hits("We use Golang, Postgres and Kafka. Experience with Django.", PROFILE)
        self.assertEqual(sorted(hits), ["Go", "Kafka", "PostgreSQL"])
        self.assertNotIn("Go", scout.keyword_hits("Good communication and Google Docs", PROFILE))

    def test_score_rewards_fit_and_freshness_and_penalises_years(self):
        fresh = scout.score({"title": "Backend Engineer", "description": "Go, Postgres, Redis, Kafka",
                             "posted": TODAY}, PROFILE, TODAY)
        stale = scout.score({"title": "Backend Engineer", "description": "Go, Postgres, Redis, Kafka",
                             "posted": TODAY - dt.timedelta(days=20)}, PROFILE, TODAY)
        senior = scout.score({"title": "Backend Engineer", "description": "Go, Postgres, Redis, Kafka. 5+ years of experience",
                              "posted": TODAY}, PROFILE, TODAY)
        self.assertGreater(fresh, stale)
        self.assertGreater(fresh, senior)
        self.assertTrue(0 <= senior <= 100 and 0 <= fresh <= 100)


class NormaliseTest(unittest.TestCase):
    def test_greenhouse(self):
        j = scout.from_greenhouse("acme", {"id": 7, "title": "SDE", "absolute_url": "https://x/7",
                                           "location": {"name": "Pune"}, "first_published": "2026-10-18T00:00:00Z",
                                           "content": "&lt;p&gt;Go &amp;amp; Postgres&lt;/p&gt;"})
        self.assertEqual(j["id"], "greenhouse:acme:7")
        self.assertEqual(j["description"], "Go & Postgres")
        self.assertEqual(j["posted_raw"], "2026-10-18T00:00:00Z")

    def test_lever(self):
        j = scout.from_lever("acme", {"id": "ab", "text": "SDE", "hostedUrl": "https://x/ab", "createdAt": 1,
                                      "categories": {"location": "Remote"}, "descriptionPlain": "Go",
                                      "lists": [{"text": "You", "content": "<li>Redis</li>"}]})
        self.assertEqual((j["id"], j["location"]), ("lever:acme:ab", "Remote"))
        self.assertIn("Redis", j["description"])

    def test_ashby(self):
        j = scout.from_ashby("acme", {"id": "z", "title": "SDE", "jobUrl": "https://x/z", "location": "Berlin",
                                      "publishedAt": "2026-10-18", "descriptionPlain": "Go",
                                      "secondaryLocations": [{"location": "Amsterdam"}]})
        self.assertEqual(j["location"], "Berlin; Amsterdam")


class DedupeTest(unittest.TestCase):
    def test_only_unseen_jobs_pass(self):
        jobs = [{"id": "a"}, {"id": "b"}]
        self.assertEqual([j["id"] for j in scout.unseen(jobs, {"a"})], ["b"])


if __name__ == "__main__":
    unittest.main()
