import json
import os
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class GitHubClient:
    def __init__(self, token=None, ttl_seconds=3600):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.ttl_seconds = ttl_seconds
        self.cache = {}

    def get(self, path, params=None):
        query = urlencode(params or {})
        cache_key = f"{path}?{query}"
        cached = self.cache.get(cache_key)
        if cached and time.time() - cached[0] < self.ttl_seconds:
            return cached[1]

        url = f"https://api.github.com{path}"
        if query:
            url = f"{url}?{query}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "navarrocarter-github-metrics",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        with urlopen(Request(url, headers=headers), timeout=15) as response:
            data = json.load(response)
        self.cache[cache_key] = (time.time(), data)
        return data

    def profile(self, username):
        return self.get(f"/users/{username}")

    def repositories(self, username):
        return self.get(
            f"/users/{username}/repos",
            {"per_page": 100, "sort": "updated", "direction": "desc", "type": "owner"},
        )

    def events(self, username):
        return self.get(f"/users/{username}/events/public", {"per_page": 100})

