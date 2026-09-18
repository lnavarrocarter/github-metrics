import json
import os

_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "profiles.json")
_cache = {"mtime": None, "data": {}}


def _load():
    try:
        mtime = os.path.getmtime(_PATH)
    except OSError:
        return {}
    if _cache["mtime"] != mtime:
        with open(_PATH, "r", encoding="utf-8") as handle:
            _cache["data"] = json.load(handle)
        _cache["mtime"] = mtime
    return _cache["data"]


def get_profile(platform, username):
    if not username:
        return None
    platform_data = _load().get(platform, {})
    for key, value in platform_data.items():
        if key.lower() == username.lower():
            return value
    return None
