from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_fly():
    return "hello from fly.io"

@app.route("/favorite/<favorite_game>")
def favorite_game(favorite_game):
    return f"<p>My favorite game is {favorite_game.title()}!</p>"
