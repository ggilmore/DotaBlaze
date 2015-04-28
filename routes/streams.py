from flask import render_template
from helpers import process_response

def register(app, match_tracker, worker):
    @app.route('/')
    def index():
        games = process_response(match_tracker.get_matches())
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
