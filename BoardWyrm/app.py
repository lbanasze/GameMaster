from flask import Flask, render_template
from markupsafe import escape
import requests

app = Flask(__name__)

@app.route("/")
def hello_fly():
    return render_template("index.html")

@app.route("/favorite/<favorite_game>")
def favorite_game(favorite_game):
    return f"<p>My favorite game is {favorite_game.title()}!</p>"

@app.route("/test/requests")
def test_requests():
    response = requests.get("https://example.com/")
    text = response.text
    return escape(text)
