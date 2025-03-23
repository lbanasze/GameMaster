from flask import Flask, render_template, request
from markupsafe import escape
from datetime import datetime
from parse import get_bgg_user_collection
from pprint import pprint
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html.jinja")


@app.route("/user")
def user():
    username = request.args.get("bgg_username", "")
    collection = get_bgg_user_collection(username)
    thumbnails = list(map(lambda item: item.get("thumbnail", ""), collection))
    # Separate the games into N groups
    game_shelves = list(
        map(lambda i: thumbnails[i : i + 7], range(0, len(thumbnails), 7))
    )

    return render_template(
        "shelf.html.jinja", game_shelves=game_shelves, username=username
    )
