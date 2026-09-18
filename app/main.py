import os

from flask import Flask, Response, jsonify, request

from app.github import GitHubClient
from app import svg
from app.profiles import get_profile
from app.whitelist import is_allowed


DEFAULT_USERNAME = os.getenv("GITHUB_USERNAME", "lnavarrocarter")
app = Flask(__name__)
client = GitHubClient()

GITHUB_CARDS = {
    "overview": lambda username, theme: svg.overview(client.profile(username), client.repositories(username), theme),
    "languages": lambda username, theme: svg.languages(client.repositories(username), theme),
    "activity": lambda username, theme: svg.activity(client.events(username), theme),
    "pulse": lambda username, theme: svg.pulse(client.repositories(username), theme),
}

# Instagram y LinkedIn no ofrecen una API pública para leer métricas de
# cualquier perfil de terceros en vivo; usan datos auto-reportados por el
# propio dueño del perfil (ver app/profiles.py y config/profiles.json).
MANUAL_PLATFORMS = {"instagram", "linkedin"}


def svg_response(content, status=200):
    return Response(content, status=status, mimetype="image/svg+xml", headers={"Cache-Control": "public, max-age=3600"})


@app.get("/status")
def healthz():
    return jsonify(status="ok", username=DEFAULT_USERNAME)


@app.get("/metrics/<card>.svg")
def legacy_card(card):
    theme = request.args.get("theme")
    handler = GITHUB_CARDS.get(card)
    if not handler:
        return svg_response(svg.message_card("Tarjeta no encontrada", f"No existe la métrica '{card}'.", theme, danger=True), status=404)
    return svg_response(handler(DEFAULT_USERNAME, theme))


@app.get("/cards/<platform>/<username>/<card>.svg")
def public_card(platform, username, card):
    theme = request.args.get("theme")

    if platform in MANUAL_PLATFORMS:
        if not is_allowed(platform, username):
            return svg_response(svg.message_card("Acceso no autorizado", f"@{username} no está en la whitelist de {platform}.", theme, danger=True), status=403)
        data = get_profile(platform, username)
        if not data:
            return svg_response(svg.message_card(f"{platform.title()} pendiente", f"@{username} aún no cargó sus datos en config/profiles.json.", theme))
        return svg_response(svg.social_profile(platform, data, theme))

    if platform != "github":
        return svg_response(svg.message_card("Plataforma no soportada", f"'{platform}' no está disponible.", theme, danger=True), status=404)

    if not is_allowed("github", username):
        return svg_response(svg.message_card("Acceso no autorizado", f"@{username} no está en la whitelist. Solicita acceso via PR.", theme, danger=True), status=403)

    handler = GITHUB_CARDS.get(card)
    if not handler:
        return svg_response(svg.message_card("Tarjeta no encontrada", f"No existe la métrica '{card}'.", theme, danger=True), status=404)

    return svg_response(handler(username, theme))


@app.errorhandler(Exception)
def handle_error(error):
    app.logger.exception("Unable to generate GitHub metrics")
    theme = request.args.get("theme")
    return svg_response(svg.message_card("Métricas no disponibles", "Vuelve a intentarlo en unos minutos.", theme, danger=True), status=503)


