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


def _live_dot(theme, x=696, y=32):
    return f'''<circle cx="{x}" cy="{y}" r="4" fill="{theme['green']}">
<animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/>
</circle>
<circle cx="{x}" cy="{y}" r="4" fill="none" stroke="{theme['green']}" stroke-width="1.5" opacity="0.6">
<animate attributeName="r" values="4;10;4" dur="2s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0.6;0;0.6" dur="2s" repeatCount="indefinite"/>
</circle>'''


def _svg(title, body, theme=None, theme_name=None):
    theme = theme or get_theme(theme_name)
    safe_title = escape(title)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title">
<title id="title">{safe_title}</title>
{_defs(theme)}
<rect width="100%" height="100%" rx="10" fill="{theme['background']}"/>
<rect x="1" y="1" width="718" height="218" rx="9" fill="none" stroke="url(#border-glow)" stroke-width="1.5"/>
<rect x="1" y="1" width="718" height="218" rx="9" fill="none" stroke="{theme['border']}"/>
<text x="32" y="43" fill="{theme['text']}" font-family="Arial, sans-serif" font-size="22" font-weight="700">{safe_title}</text>
{_live_dot(theme)}
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
        _metric(32, "repositorios públicos", profile.get("public_repos", 0), theme),
        _metric(210, "seguidores", profile.get("followers", 0), theme, theme["green"]),
        _metric(370, "estrellas recibidas", stars, theme, theme["orange"]),
        _metric(565, "forks", forks, theme),
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
    return _svg(title, body, theme)

