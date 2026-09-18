import json
import os
import time

_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "whitelist.json")
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


def is_allowed(platform, username):
    if not username:
        return False
    allowed = _load().get(platform, [])
    return username.lower() in {entry.lower() for entry in allowed}


def allowed_usernames(platform):
    return list(_load().get(platform, []))
