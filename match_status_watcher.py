from Helpers import processResponse

import requests
import time

dota2_url = "https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v0001/?key=12B9C2C08AAC635D3A305D7D26793738"

class MatchTracker(object):

    def __init__(self, url=dota2_url):
        self.url = url
        self.matches = self.get_matches()
        self.match_change_history = []

    def get_match_updates(self):
        old_match_id_set = {ent[u"match_id"] for ent in self.matches}
        #map(self.get_match_id(), self.matches)
        self.matches = self.get_matches()
        new_match_id_set = {ent[u"match_id"] for ent in self.matches}
        #map(self.get_match_id(), self.matches)
        return (
            old_match_id_set - new_match_id_set,
            new_match_id_set - old_match_id_set)

    def get_matches(self):
        r = requests.get(self.url)
        return [ent for ent in r.json()[u"result"][u"games"]]

    def get_match_id(self, match):
        return match[u"match_id"]

    def get_match_teams(self, match):
        r = match[u"radiant_team"]
        d = match[u"dire_team"]
        return  {"radiant_team_name": r[u"team_name"],
                "radiant_team_id": r[u"team_id"],
                "dire_team_name": d[u"team_name"],
                "dire_team_id": d[u"team_id"]}

    def push_to_match_change_history(self, update):
        time_stamp = time.time()
        update_list = []
        for match in update[0]: # matches that ended
            match_dict = {"match_id": match, "time_stamp": time_stamp, "just_ended": True}
            update_list.append(match_dict)
        for match in update[1]: # matches that started
            match_dict = {"match_id": match, "time_stamp": time_stamp, "just_ended": False}
            update_list.append(match_dict)
        self.match_change_history.extend(update_list)

    def make_match_status_change_event(self, match_updates):
        time_stamp = time.time()
        update_list = []
        for match in match_updates[0]: # matches that ended
            update_list.append(self.generate_event_info(match, True))
        for match in match_updates[1]: # matches that started
            update_list.append(self.generate_event_info(match, False))
        self.match_change_history.extend(update_list)

    def generate_event_info(self, match, isEnded):
        event_info = {"time_stamp": time.time()}
        event_info.update(get_match_id(match))
        event_info.update(get_match_teams(match))
        event_info.update({"description": "event happened"})
        return event_info

    def get_match_change_history(self):
        return self.match_change_history
