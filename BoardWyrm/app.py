from flask import Flask, render_template, request
from markupsafe import escape
from datetime import datetime
import requests

app = Flask(__name__)

@app.context_processor
def inject_now():
    return {'current_year': datetime.utcnow().year}

@app.route("/")
def index():
    return render_template("child.html.jinja")

@app.route("/user")
def user():
    username = request.args.get("bgg_username", "")
    subtype = request.args.get("subtype", "")
    resp = requests.get(f"https://boardgamegeek.com/xmlapi2/collection?username={username}&own=1&subtype={subtype}&stats=1")
    text = resp.text
    print(f"resp: [{resp}]")
    return escape(text)

@app.route("/favorite/<favorite_game>")
def favorite_game(favorite_game):
    return f"<p>My favorite game is {favorite_game.title()}!</p>"

@app.route("/test/requests")
def test_requests():
    response = requests.get("https://example.com/")
    text = response.text
    return escape(text)
