from flask import Flask, render_template, request, jsonify
from markupsafe import escape
from datetime import datetime
from parse import get_bgg_user_collection, get_bgg_game_details
from pprint import pprint
from models.bgg_game_details import BggGameDetails

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


@app.route("/debug-details/<username>")
def game_details(username):
    collection = get_bgg_user_collection(username)
    game_ids =  list(map(lambda item: int(item.get("objectid", "")), collection))
    results = get_bgg_game_details(game_ids)
    results = list(filter(lambda r:  r.get("error", None) == None, results))
    details = [BggGameDetails.model_validate(detail) for detail in results]
    pprint(details)
    render = [d.model_dump() for d in details]
    return jsonify(render)
