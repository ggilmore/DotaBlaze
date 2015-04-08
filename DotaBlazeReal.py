from flask import Flask, render_template
import requests
from Helpers import processResponse


app = Flask(__name__)


@app.route('/')
def index():
    r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v0001/?key=12B9C2C08AAC635D3A305D7D26793738")
    games = processResponse(r.json()[u"result"][u"games"])
    games
    return render_template("index.html", games=games)

if __name__ == '__main__':
    app.run(debug=True)

