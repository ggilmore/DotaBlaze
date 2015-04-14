from flask import Flask, render_template
import requests
from Helpers import processResponse
from MatchTrackerWorker import MatchTrackerWorker
from match_status_watcher import MatchTracker


app = Flask(__name__)

match_tracker = MatchTracker()

worker = MatchTrackerWorker(match_tracker, 5)
worker.start()

@app.route('/')
def index():
    r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v0001/?key=12B9C2C08AAC635D3A305D7D26793738")
    games = processResponse(r.json()[u"result"][u"games"])
    return render_template("index.html", games=games)

@app.route('/matches')
def matches():
    match_updates = match_tracker.get_match_updates()
    match_tracker.push_to_match_change_history(match_updates)
    return str(worker.get_match_change_history())
    # return render_template("matches.html", updates=match_updates)

@app.route('/events')
def events():
    events = worker.get_match_change_history()
    return render_template("event-stream.html", events=events)

if __name__ == '__main__':
    app.run(debug=True)

