__author__ = 'gmgilmore'

from threading import Thread
import time

from match_status_watcher import MatchTracker

class MatchTrackerWorker(Thread):
    def __init__(self, tracker, interval):
        Thread.__init__(self)
        self.tracker = tracker
        self.interval = interval

    def run(self):
        while True:
            time.sleep(self.interval)
            self.tracker.push_to_match_change_history(self.tracker.get_match_updates())
            # print str(self.get_match_change_history())


    def get_match_change_history(self):
        return self.tracker.get_match_change_history()