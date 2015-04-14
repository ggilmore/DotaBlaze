from Helpers import processResponse

import requests
import time

dota2_url = "https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v0001/?key=12B9C2C08AAC635D3A305D7D26793738"

class MatchTracker(object):

    def __init__(self, url=dota2_url):
        self.url = url
        self.match_ids = self.get_matches()
        self.match_change_history = []

    def get_match_updates(self):
        old_match_ids = self.match_ids
        self.match_ids = self.get_matches()
        return (
            old_match_ids - self.match_ids,
            self.match_ids - old_match_ids)

    def get_matches(self):
        r = requests.get(self.url)
        return {ent[u"match_id"] for ent in r.json()[u"result"][u"games"]}

    def push_to_match_change_history(self, update):
        time_stamp = time.gmtime()
        update_list = []
        for match in update[0]: # matches that ended
            match_dict = {"match_id": match, "time_stamp": time_stamp, "just_ended": True}
            update_list.append(match_dict)
        for match in update[1]: # matches that started
            match_dict = {"match_id": match, "time_stamp": time_stamp, "just_ended": False}
            update_list.append(match_dict)
        self.match_change_history.extend(update_list)

    def get_match_change_history(self):
        return self.match_change_history
