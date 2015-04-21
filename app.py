from flask import Flask, render_template
from helpers import process_response
from match_tracker_worker import MatchTrackerWorker
from match_status_watcher import MatchTracker

from routes import streams


# setup app
app = Flask(__name__)
app.config.from_pyfile('settings.py')

# create workers
match_tracker = MatchTracker(url=app.config['DOTA2_URL'],
                             api_key=app.config['DOTA2_API_KEY'])
worker = MatchTrackerWorker(match_tracker, 5)

# register routes
streams.register(app, match_tracker, worker)

if __name__ == '__main__':
    worker.start()
    app.run(app.config['HOST'], app.config['PORT'], debug=True)
