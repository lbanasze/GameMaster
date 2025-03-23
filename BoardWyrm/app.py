from flask import Flask, render_template, request
from markupsafe import escape
from datetime import datetime
from parse import get_bgg_user_collection
from pprint import pprint
import requests

app = Flask(__name__)


@app.context_processor
def inject_now():
    return {"current_year": datetime.utcnow().year}


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
    # meta = list(
    #     map(
    #         lambda item: {
    #             "image": item.get("image", ""),
    #             "objectid": item.get("objectid"),
    #         },
    #         collection,
    #     )
    # )
    # images_html = list(map(lambda item: f'<img src="{item.get("thumbnail", "")}" alt="{item.get("name", "")}">', collection))
    #
    # Split the games into shelves of 5 games max
    game_shelves = []
    for i in range(0, len(thumbnails), 5):
        game_shelves.append(thumbnails[i : i + 5])

    return render_template("shelf.html.jinja", game_shelves=game_shelves)


@app.route("/game")
def game_id():
    game_id = request.args.get("game_id", "")
    details = parse.get_bgg_game_details(game_id)
    return escape(details)


@app.route("/favorite/<favorite_game>")
def favorite_game(favorite_game):
    return f"<p>My favorite game is {favorite_game.title()}!</p>"


@app.route("/test/requests")
def test_requests():
    response = requests.get("https://example.com/")
    text = response.text
    return escape(text)
