import os

from flask import Flask, Response, jsonify

from app.github import GitHubClient
from app import svg


USERNAME = os.getenv("GITHUB_USERNAME", "lnavarrocarter")
app = Flask(__name__)
client = GitHubClient()


def svg_response(content):
    return Response(content, mimetype="image/svg+xml", headers={"Cache-Control": "public, max-age=3600"})


@app.get("/healthz")
def healthz():
    return jsonify(status="ok", username=USERNAME)


@app.get("/metrics/overview.svg")
def overview():
    return svg_response(svg.overview(client.profile(USERNAME), client.repositories(USERNAME)))


@app.get("/metrics/languages.svg")
def languages():
    return svg_response(svg.languages(client.repositories(USERNAME)))


@app.get("/metrics/activity.svg")
def activity():
    return svg_response(svg.activity(client.events(USERNAME)))


@app.get("/metrics/pulse.svg")
def pulse():
    return svg_response(svg.pulse(client.repositories(USERNAME)))


@app.errorhandler(Exception)
def handle_error(error):
    app.logger.exception("Unable to generate GitHub metrics")
    return Response(svg._svg("Métricas no disponibles", '<text x="32" y="90" fill="#ff7b72" font-family="Arial, sans-serif" font-size="16">Vuelve a intentarlo en unos minutos.</text>'), status=503, mimetype="image/svg+xml")

