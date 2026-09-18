from collections import Counter
from html import escape

from app.themes import get_theme


WIDTH = 720
HEIGHT = 220


def _defs(theme):
    return f'''<defs>
<linearGradient id="border-glow" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="{theme['accent']}" stop-opacity="0"/>
  <stop offset="50%" stop-color="{theme['accent']}" stop-opacity="0.9"/>
  <stop offset="100%" stop-color="{theme['accent2']}" stop-opacity="0"/>
  <animate attributeName="x1" values="-40%;100%" dur="4s" repeatCount="indefinite"/>
  <animate attributeName="x2" values="60%;200%" dur="4s" repeatCount="indefinite"/>
</linearGradient>
</defs>'''


def _live_dot(theme, x=684, y=32):
    return f'''<circle cx="{x}" cy="{y}" r="4" fill="{theme['green']}">
<animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/>
</circle>
<circle cx="{x}" cy="{y}" r="4" fill="none" stroke="{theme['green']}" stroke-width="1.5" opacity="0.6">
<animate attributeName="r" values="4;10;4" dur="2s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0.6;0;0.6" dur="2s" repeatCount="indefinite"/>
</circle>
<text x="{x - 12}" y="36" fill="{theme['green']}" font-family="Arial, sans-serif" font-size="11" text-anchor="end">en vivo</text>'''


def _manual_dot(theme, x=684, y=32):
    return f'''<circle cx="{x}" cy="{y}" r="4" fill="{theme['muted']}"/>
<text x="{x - 12}" y="36" fill="{theme['muted']}" font-family="Arial, sans-serif" font-size="11" text-anchor="end">manual</text>'''


def _indicator(theme, mode):
    if mode == "manual":
        return _manual_dot(theme)
    if mode == "live":
        return _live_dot(theme)
    return ""


def _avatar(url, theme, x=32, y=58, size=64):
    if not url:
        return ""
    clip_id = "avatar-clip"
    radius = size / 2
    cx = x + radius
    cy = y + radius
    return f'''<defs>
<clipPath id="{clip_id}"><circle cx="{cx}" cy="{cy}" r="{radius}"/></clipPath>
</defs>
<circle cx="{cx}" cy="{cy}" r="{radius + 2}" fill="none" stroke="{theme['accent']}" stroke-width="2"/>
<image href="{escape(url)}" x="{x}" y="{y}" width="{size}" height="{size}" clip-path="url(#{clip_id})" preserveAspectRatio="xMidYMid slice"/>'''


def _monogram(label, theme, x=32, y=58, size=64):
    cx = x + size / 2
    cy = y + size / 2
    return f'''<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size / 4}" fill="{theme['panel']}" stroke="{theme['accent']}" stroke-width="2"/>
<text x="{cx}" y="{cy + 7}" fill="{theme['accent']}" font-family="Arial, sans-serif" font-size="22" font-weight="700" text-anchor="middle">{escape(label)}</text>'''


def _svg(title, body, theme=None, theme_name=None, indicator="live"):
    theme = theme or get_theme(theme_name)
    safe_title = escape(title)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title">
<title id="title">{safe_title}</title>
{_defs(theme)}
<rect width="100%" height="100%" rx="10" fill="{theme['background']}"/>
<rect x="1" y="1" width="718" height="218" rx="9" fill="none" stroke="url(#border-glow)" stroke-width="1.5"/>
<rect x="1" y="1" width="718" height="218" rx="9" fill="none" stroke="{theme['border']}"/>
<text x="32" y="43" fill="{theme['text']}" font-family="Arial, sans-serif" font-size="22" font-weight="700">{safe_title}</text>
{_indicator(theme, indicator)}
{body}</svg>'''


def _metric(x, label, value, theme, color=None):
    color = color or theme["accent"]
    return f'''<text x="{x}" y="103" fill="{color}" font-family="Arial, sans-serif" font-size="35" font-weight="700">{escape(str(value))}</text>
<text x="{x}" y="132" fill="{theme['muted']}" font-family="Arial, sans-serif" font-size="14">{escape(label)}</text>'''


def _footer(text, theme):
    return f'<text x="32" y="183" fill="{theme["muted"]}" font-family="Arial, sans-serif" font-size="14">{escape(text)}</text>'


def overview(profile, repositories, theme_name=None):
    theme = get_theme(theme_name)
    stars = sum(repo.get("stargazers_count", 0) for repo in repositories)
    forks = sum(repo.get("forks_count", 0) for repo in repositories)
    body = "".join((
        _avatar(profile.get("avatar_url"), theme),
        _metric(130, "repositorios públicos", profile.get("public_repos", 0), theme),
        _metric(310, "seguidores", profile.get("followers", 0), theme, theme["green"]),
        _metric(470, "estrellas recibidas", stars, theme, theme["orange"]),
        _metric(620, "forks", forks, theme),
        _footer(f'@{profile.get("login", "")} · actualizado automáticamente', theme),
    ))
    return _svg("GitHub overview", body, theme)


def languages(repositories, theme_name=None):
    theme = get_theme(theme_name)
    counts = Counter(repo.get("language") for repo in repositories if repo.get("language"))
    top = counts.most_common(5)
    total = sum(counts.values()) or 1
    y = 81
    rows = []
    for index, (language, count) in enumerate(top):
        width = int(420 * count / total)
        delay = f'{index * 0.1:.1f}s'
        rows.append(f'<text x="32" y="{y}" fill="{theme["text"]}" font-family="Arial, sans-serif" font-size="15">{escape(language)}</text>')
        rows.append(f'<rect x="190" y="{y - 14}" width="420" height="12" rx="6" fill="{theme["panel"]}"/>')
        rows.append(
            f'<rect x="190" y="{y - 14}" width="0" height="12" rx="6" fill="{theme["accent"]}">'
            f'<animate attributeName="width" from="0" to="{width}" dur="1s" begin="{delay}" fill="freeze"/>'
            f'</rect>'
        )
        rows.append(f'<text x="628" y="{y}" fill="{theme["muted"]}" font-family="Arial, sans-serif" font-size="14">{count} repos</text>')
        y += 27
    body = "".join(rows) or f'<text x="32" y="88" fill="{theme["muted"]}" font-family="Arial, sans-serif" font-size="15">Sin datos de lenguaje público.</text>'
    return _svg("Lenguajes más usados", body, theme)


def activity(events, theme_name=None):
    theme = get_theme(theme_name)
    types = Counter(event.get("type", "Activity") for event in events)
    labels = {"PushEvent": "pushes", "PullRequestEvent": "pull requests", "IssuesEvent": "issues", "CreateEvent": "creaciones"}
    top = types.most_common(4)
    body = []
    for index, (event_type, count) in enumerate(top):
        x = 32 + index * 170
        color = theme["green"] if index == 0 else theme["accent"]
        body.append(_metric(x, labels.get(event_type, event_type.replace("Event", "").lower()), count, theme, color))
    body.append(_footer("Muestra basada en los últimos eventos públicos de GitHub.", theme))
    return _svg("Actividad reciente", "".join(body), theme)


def pulse(repositories, theme_name=None):
    theme = get_theme(theme_name)
    active = sum(1 for repo in repositories if not repo.get("archived") and not repo.get("fork"))
    archived = sum(1 for repo in repositories if repo.get("archived"))
    updated = sum(1 for repo in repositories if repo.get("pushed_at"))
    body = "".join((
        _metric(32, "proyectos activos", active, theme, theme["green"]),
        _metric(235, "repos con actividad", updated, theme),
        _metric(470, "proyectos archivados", archived, theme, theme["orange"]),
        _footer("Open-source pulse · alcance y mantenimiento del portafolio", theme),
    ))
    return _svg("Open-source pulse", body, theme)


def message_card(title, message, theme_name=None, danger=False):
    theme = get_theme(theme_name)
    color = theme["danger"] if danger else theme["muted"]
    body = f'<text x="32" y="90" fill="{color}" font-family="Arial, sans-serif" font-size="16">{escape(message)}</text>'
    return _svg(title, body, theme, indicator=None)


PLATFORM_LABELS = {"instagram": "IG", "linkedin": "in"}
PLATFORM_TITLES = {"instagram": "Instagram", "linkedin": "LinkedIn"}


def social_profile(platform, data, theme_name=None):
    theme = get_theme(theme_name)
    title = PLATFORM_TITLES.get(platform, platform.title())
    monogram = PLATFORM_LABELS.get(platform, platform[:2].upper())

    def fmt(value):
        return str(value) if value is not None else "—"

    if platform == "instagram":
        metrics = [("publicaciones", fmt(data.get("posts"))), ("seguidores", fmt(data.get("followers")))]
    elif platform == "linkedin":
        metrics = [("conexiones", fmt(data.get("connections")))]
    else:
        metrics = []

    name = data.get("display_name") or data.get("handle", "")
    handle = data.get("handle", "")
    subtitle = data.get("headline") or data.get("bio") or ""

    rows = [
        _monogram(monogram, theme, x=32, y=54, size=56),
        f'<text x="104" y="72" fill="{theme["text"]}" font-family="Arial, sans-serif" font-size="18" font-weight="700">{escape(name)}</text>',
        f'<text x="104" y="92" fill="{theme["muted"]}" font-family="Arial, sans-serif" font-size="13">@{escape(handle)}</text>',
    ]
    if subtitle:
        rows.append(f'<text x="104" y="110" fill="{theme["muted"]}" font-family="Arial, sans-serif" font-size="12">{escape(subtitle)}</text>')

    x = 32
    for label, value in metrics:
        rows.append(f'<text x="{x}" y="152" fill="{theme["accent"]}" font-family="Arial, sans-serif" font-size="28" font-weight="700">{escape(value)}</text>')
        rows.append(f'<text x="{x}" y="172" fill="{theme["muted"]}" font-family="Arial, sans-serif" font-size="13">{escape(label)}</text>')
        x += 200

    updated_at = data.get("updated_at", "")
    rows.append(f'<text x="32" y="197" fill="{theme["muted"]}" font-family="Arial, sans-serif" font-size="12">Datos auto-reportados · actualizado el {escape(updated_at)}</text>')

    return _svg(title, "".join(rows), theme, indicator="manual")

