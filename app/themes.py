THEMES = {
    "tokyonight": {
        "background": "#131622",
        "panel": "#1d2130",
        "border": "#2e3548",
        "text": "#e7eaf0",
        "muted": "#9ba5ba",
        "accent": "#70a5fd",
        "accent2": "#bb9af7",
        "green": "#56d364",
        "orange": "#f2cc60",
        "danger": "#ff7b72",
    },
    "sunset": {
        "background": "#1f1410",
        "panel": "#2b1c16",
        "border": "#4a2e22",
        "text": "#fbeee0",
        "muted": "#d9a98b",
        "accent": "#ff9457",
        "accent2": "#ff6b81",
        "green": "#7bd88f",
        "orange": "#ffce54",
        "danger": "#ff6b6b",
    },
    "forest": {
        "background": "#0f1a14",
        "panel": "#16261c",
        "border": "#25402f",
        "text": "#e5f2e8",
        "muted": "#9dbfab",
        "accent": "#4fd1a5",
        "accent2": "#8ce99a",
        "green": "#63e6be",
        "orange": "#f2cc60",
        "danger": "#ff8787",
    },
    "mono": {
        "background": "#111111",
        "panel": "#1c1c1c",
        "border": "#333333",
        "text": "#f2f2f2",
        "muted": "#a0a0a0",
        "accent": "#ffffff",
        "accent2": "#cccccc",
        "green": "#e0e0e0",
        "orange": "#b0b0b0",
        "danger": "#ff5c5c",
    },
}

DEFAULT_THEME = "tokyonight"


def get_theme(name):
    return THEMES.get((name or "").lower(), THEMES[DEFAULT_THEME])
