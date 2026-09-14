from collections import Counter
from html import escape


WIDTH = 720
HEIGHT = 220
BACKGROUND = "#131622"
PANEL = "#1d2130"
TEXT = "#e7eaf0"
MUTED = "#9ba5ba"
ACCENT = "#70a5fd"
GREEN = "#56d364"
ORANGE = "#f2cc60"


def _svg(title, body):
    safe_title = escape(title)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title">
<title id="title">{safe_title}</title>
<rect width="100%" height="100%" rx="10" fill="{BACKGROUND}"/>
<rect x="1" y="1" width="718" height="218" rx="9" fill="none" stroke="#2e3548"/>
<text x="32" y="43" fill="{TEXT}" font-family="Arial, sans-serif" font-size="22" font-weight="700">{safe_title}</text>
{body}</svg>'''


def _metric(x, label, value, color=ACCENT):
    return f'''<text x="{x}" y="103" fill="{color}" font-family="Arial, sans-serif" font-size="35" font-weight="700">{escape(str(value))}</text>
<text x="{x}" y="132" fill="{MUTED}" font-family="Arial, sans-serif" font-size="14">{escape(label)}</text>'''


def overview(profile, repositories):
    stars = sum(repo.get("stargazers_count", 0) for repo in repositories)
    forks = sum(repo.get("forks_count", 0) for repo in repositories)
    body = "".join((
        _metric(32, "repositorios públicos", profile.get("public_repos", 0)),
        _metric(210, "seguidores", profile.get("followers", 0), GREEN),
        _metric(370, "estrellas recibidas", stars, ORANGE),
        _metric(565, "forks", forks),
        f'<text x="32" y="183" fill="{MUTED}" font-family="Arial, sans-serif" font-size="14">@{escape(profile.get("login", ""))} · actualizado automáticamente</text>',
    ))
    return _svg("GitHub overview", body)


def languages(repositories):
    counts = Counter(repo.get("language") for repo in repositories if repo.get("language"))
    top = counts.most_common(5)
    total = sum(counts.values()) or 1
    y = 81
    rows = []
    for language, count in top:
        width = int(420 * count / total)
        rows.append(f'<text x="32" y="{y}" fill="{TEXT}" font-family="Arial, sans-serif" font-size="15">{escape(language)}</text>')
        rows.append(f'<rect x="190" y="{y - 14}" width="420" height="12" rx="6" fill="{PANEL}"/>')
        rows.append(f'<rect x="190" y="{y - 14}" width="{width}" height="12" rx="6" fill="{ACCENT}"/>')
        rows.append(f'<text x="628" y="{y}" fill="{MUTED}" font-family="Arial, sans-serif" font-size="14">{count} repos</text>')
        y += 27
    return _svg("Lenguajes más usados", "".join(rows) or f'<text x="32" y="88" fill="{MUTED}" font-family="Arial, sans-serif" font-size="15">Sin datos de lenguaje público.</text>')


def activity(events):
    types = Counter(event.get("type", "Activity") for event in events)
    labels = {"PushEvent": "pushes", "PullRequestEvent": "pull requests", "IssuesEvent": "issues", "CreateEvent": "creaciones"}
    top = types.most_common(4)
    body = []
    for index, (event_type, count) in enumerate(top):
        x = 32 + index * 170
        body.append(_metric(x, labels.get(event_type, event_type.replace("Event", "").lower()), count, GREEN if index == 0 else ACCENT))
    body.append(f'<text x="32" y="183" fill="{MUTED}" font-family="Arial, sans-serif" font-size="14">Muestra basada en los últimos eventos públicos de GitHub.</text>')
    return _svg("Actividad reciente", "".join(body))


def pulse(repositories):
    releases = sum(1 for repo in repositories if not repo.get("archived") and not repo.get("fork"))
    archived = sum(1 for repo in repositories if repo.get("archived"))
    updated = sum(1 for repo in repositories if repo.get("pushed_at"))
    body = "".join((
        _metric(32, "proyectos activos", releases, GREEN),
        _metric(235, "repos con actividad", updated, ACCENT),
        _metric(470, "proyectos archivados", archived, ORANGE),
        f'<text x="32" y="183" fill="{MUTED}" font-family="Arial, sans-serif" font-size="14">Open-source pulse · alcance y mantenimiento del portafolio</text>',
    ))
    return _svg("Open-source pulse", body)

