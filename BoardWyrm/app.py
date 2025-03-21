from flask import Flask, render_template
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

@app.route("/favorite/<favorite_game>")
def favorite_game(favorite_game):
    return f"<p>My favorite game is {favorite_game.title()}!</p>"

@app.route("/test/requests")
def test_requests():
    response = requests.get("https://example.com/")
    text = response.text
    return escape(text)
