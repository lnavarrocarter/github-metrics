import unittest

from app import svg
from app.profiles import get_profile
from app.whitelist import is_allowed


class MetricsSvgTests(unittest.TestCase):
    def setUp(self):
        self.profile = {"login": "lnavarrocarter", "public_repos": 12, "followers": 8, "avatar_url": "https://avatars.githubusercontent.com/u/1"}
        self.repositories = [
            {"language": "TypeScript", "stargazers_count": 7, "forks_count": 2, "archived": False, "pushed_at": "2026-09-01T00:00:00Z"},
            {"language": "Python", "stargazers_count": 3, "forks_count": 1, "archived": True, "pushed_at": "2026-09-02T00:00:00Z"},
        ]

    def test_overview_includes_profile_metrics(self):
        card = svg.overview(self.profile, self.repositories)
        self.assertIn("GitHub overview", card)
        self.assertIn("10", card)
        self.assertIn("image/svg+xml", "image/svg+xml")

    def test_overview_embeds_avatar_image(self):
        card = svg.overview(self.profile, self.repositories)
        self.assertIn("<image href=", card)
        self.assertIn("avatars.githubusercontent.com", card)

    def test_languages_includes_detected_languages(self):
        card = svg.languages(self.repositories)
        self.assertIn("TypeScript", card)
        self.assertIn("Python", card)

    def test_activity_and_pulse_render_svg(self):
        events = [{"type": "PushEvent"}, {"type": "PushEvent"}, {"type": "IssuesEvent"}]
        self.assertIn("Actividad reciente", svg.activity(events))
        self.assertIn("Open-source pulse", svg.pulse(self.repositories))

    def test_theme_changes_background_color(self):
        default_card = svg.overview(self.profile, self.repositories)
        sunset_card = svg.overview(self.profile, self.repositories, theme_name="sunset")
        self.assertNotEqual(default_card, sunset_card)
        self.assertIn("#1f1410", sunset_card)

    def test_unknown_theme_falls_back_to_default(self):
        card = svg.overview(self.profile, self.repositories, theme_name="does-not-exist")
        self.assertIn("#131622", card)

    def test_message_card_renders_danger_color(self):
        card = svg.message_card("Acceso no autorizado", "sin acceso", danger=True)
        self.assertIn("Acceso no autorizado", card)
        self.assertIn("#ff7b72", card)

    def test_social_profile_renders_instagram_card(self):
        data = {"display_name": "Nacho", "handle": "lnavarrocarter", "bio": "dev", "followers": 100, "posts": 10, "updated_at": "2026-09-18"}
        card = svg.social_profile("instagram", data, None)
        self.assertIn("Instagram", card)
        self.assertIn("@lnavarrocarter", card)
        self.assertIn("100", card)
        self.assertIn("manual", card)

    def test_social_profile_handles_missing_numbers(self):
        data = {"display_name": "Nacho", "handle": "lnavarrocarter", "connections": None, "updated_at": "2026-09-18"}
        card = svg.social_profile("linkedin", data, None)
        self.assertIn("LinkedIn", card)
        self.assertIn("—", card)


class WhitelistTests(unittest.TestCase):
    def test_seeded_github_username_is_allowed(self):
        self.assertTrue(is_allowed("github", "lnavarrocarter"))

    def test_unknown_username_is_rejected(self):
        self.assertFalse(is_allowed("github", "someone-not-registered"))

    def test_unknown_platform_is_rejected(self):
        self.assertFalse(is_allowed("tiktok", "lnavarrocarter"))

    def test_seeded_instagram_and_linkedin_usernames_are_allowed(self):
        self.assertTrue(is_allowed("instagram", "lnavarrocarter"))
        self.assertTrue(is_allowed("linkedin", "lnavarrocarter"))


class ProfilesTests(unittest.TestCase):
    def test_get_profile_returns_seeded_instagram_profile(self):
        profile = get_profile("instagram", "lnavarrocarter")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["handle"], "lnavarrocarter")

    def test_get_profile_returns_none_when_missing(self):
        self.assertIsNone(get_profile("instagram", "someone-else"))
        self.assertIsNone(get_profile("unknown-platform", "lnavarrocarter"))


if __name__ == "__main__":
    unittest.main()
