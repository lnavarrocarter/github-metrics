import unittest

from app import svg


class MetricsSvgTests(unittest.TestCase):
    def setUp(self):
        self.profile = {"login": "lnavarrocarter", "public_repos": 12, "followers": 8}
        self.repositories = [
            {"language": "TypeScript", "stargazers_count": 7, "forks_count": 2, "archived": False, "pushed_at": "2026-09-01T00:00:00Z"},
            {"language": "Python", "stargazers_count": 3, "forks_count": 1, "archived": True, "pushed_at": "2026-09-02T00:00:00Z"},
        ]

    def test_overview_includes_profile_metrics(self):
        card = svg.overview(self.profile, self.repositories)
        self.assertIn("GitHub overview", card)
        self.assertIn("10", card)
        self.assertIn("image/svg+xml", "image/svg+xml")

    def test_languages_includes_detected_languages(self):
        card = svg.languages(self.repositories)
        self.assertIn("TypeScript", card)
        self.assertIn("Python", card)

    def test_activity_and_pulse_render_svg(self):
        events = [{"type": "PushEvent"}, {"type": "PushEvent"}, {"type": "IssuesEvent"}]
        self.assertIn("Actividad reciente", svg.activity(events))
        self.assertIn("Open-source pulse", svg.pulse(self.repositories))


if __name__ == "__main__":
    unittest.main()
