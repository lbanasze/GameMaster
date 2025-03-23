from flask import Flask, render_template, request
from markupsafe import escape
from datetime import datetime
from parse import get_bgg_user_collection
from pprint import pprint
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("child.html.jinja")


@app.route("/user")
def user():
    username = request.args.get("bgg_username", "")
    collection = get_bgg_user_collection(username)
    for item in collection:
        pprint(item)
    thumbnails = list(map(lambda item: item.get("thumbnail", ""), collection))
    game_shelves = []
    for i in range(0, len(thumbnails), 7):
        game_shelves.append(thumbnails[i : i + 7])

    return render_template(
        "shelf.html.jinja", game_shelves=game_shelves, username=username
    )
