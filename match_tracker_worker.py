__author__ = 'gmgilmore'

from threading import Thread
import time

from match_status_watcher import MatchTracker

class MatchTrackerWorker(Thread):
    def __init__(self, tracker, interval):
        Thread.__init__(self)
        self.daemon = True
        self.tracker = tracker
        self.interval = interval

    def run(self):
        while True:
            time.sleep(self.interval)
            tuples = self.tracker.get_match_updates()
            info = self.tracker.generate_match_update_event_info(tuples)
            self.tracker.push_to_match_change_history(info)

    def get_match_change_history(self):
        return self.tracker.get_match_change_history()

if __name__ == "__main__":
    a = MatchTrackerWorker(MatchTracker(), 5)
    a.start()
    while True:
        pass
