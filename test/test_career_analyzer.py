
import unittest

from career_analyzer import analyze_career_profile


class TestCareerAnalyzer(unittest.TestCase):

    def test_analysis_returns_results(self):
        results = analyze_career_profile(
            ["Python", "SQL", "Java"],
            ["Artificial Intelligence", "Data Science"]
        )

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_career_result_has_required_fields(self):
        results = analyze_career_profile(
            ["Python", "SQL"],
            ["Artificial Intelligence"]
        )

        required_fields = [
            "career",
            "description",
            "match_percentage",
            "skill_score",
            "interest_score",
            "matched_skills",
            "missing_skills",
            "matched_interests",
            "projects"
        ]

        for result in results:
            for field in required_fields:
                self.assertIn(field, result)

    def test_match_percentage_is_valid(self):
        results = analyze_career_profile(
            ["Python", "Machine Learning"],
            ["Artificial Intelligence"]
        )

        for result in results:
            self.assertGreaterEqual(result["match_percentage"], 0)
            self.assertLessEqual(result["match_percentage"], 100)

    def test_empty_skills_are_handled(self):
        results = analyze_career_profile([], [])

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)


if __name__ == "__main__":
    unittest.main()

