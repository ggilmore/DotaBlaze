import requests
import time
from event_types import EventType, generate_description
from game import Game


class MatchTracker(object):
    def __init__(self, url, api_key):
        self.url = url + api_key
        self.matches = self.get_matches()
        self.match_change_history = []
        # dict of game_id -> Game class
        self.games = {}

    def make_game(self, id, radiant_team_name="radiant-unknown", dire_team_name="dire-unknown"):
        game = Game(id, radiant_team_name, dire_team_id)
        self.games[id] = game

    def get_game_events(self, id):
        if id in self.games:
            return self.games[id].get_game_events()
        else:
            return [(EventType.GAME_OVER, generate_description(EventType.GAME_OVER, {"id": id}))]

    def get_match_updates(self):
        old_match_id_set = {ent[u"match_id"] for ent in self.matches}
        old_matches = self.matches
        # map(self.get_match_id(), self.matches)
        self.matches = self.get_matches()
        new_match_id_set = {ent[u"match_id"] for ent in self.matches}
        # map(self.get_match_id(), self.matches)
        ended_match_ids = old_match_id_set - new_match_id_set
        new_match_ids = new_match_id_set - old_match_id_set
        return ((ended_match_ids, [match for match in old_matches if match["match_id"] in ended_match_ids]),
                (new_match_ids, [match for match in self.matches if match["match_id"] in new_match_ids]))

    def get_matches(self):
        r = requests.get(self.url)
        return [ent for ent in r.json()[u"result"][u"games"]]

    def get_match_id(self, match):
        return match[u"match_id"]

    def get_match_teams(self, match):
        fail_safe_dict = {u"team_name": "No Team Name", u"team_id": "0"}

        r = match.get(u"radiant_team", fail_safe_dict)
        d = match.get(u"dire_team", fail_safe_dict)

        return {"radiant_team_name": r[u"team_name"],
                "radiant_team_id": r[u"team_id"],
                "dire_team_name": d[u"team_name"],
                "dire_team_id": d[u"team_id"]}

    def push_to_match_change_history(self, update_list):
        # time_stamp = time.time()
        # update_list = []
        # for match in update[0]: # matches that ended
        # match_dict = {"match_id": match, "time_stamp": time_stamp, "just_ended": True}
        #     update_list.append(match_dict)
        # for match in update[1]: # matches that started
        #     match_dict = {"match_id": match, "time_stamp": time_stamp, "just_ended": False}
        #     update_list.append(match_dict)
        self.match_change_history.extend(update_list)

    def generate_match_update_event_info(self, match_tuples):
        result = []
        for match in match_tuples[0][1]:
            result.append(self.generate_event_info(match, event_types.EventType.MATCH_ENDED))
        for match in match_tuples[1][1]:
            result.append(self.generate_event_info(match, event_types.EventType.MATCH_STARTED))
        return result

    def make_match_status_change_event(self, match_update_list):
        # update_list = []
        # for match in match_updates[0]: # matches that ended
        # update_list.append(self.generate_event_info(match, EventType.MATCH_STARTED))
        # for match in match_updates[1]: # matches that started
        #     update_list.append(self.generate_event_info(match, EventType.MATCH_ENDED))
        self.match_change_history.extend(match_update_list)

    def generate_event_info(self, match, event_type):
        event_info = {"time_stamp": time.time()}
        event_info.update({"match_id": self.get_match_id(match)})
        event_info.update(self.get_match_teams(match))

        event_info.update({"description": event_types.generate_description(event_type, event_info["radiant_team_name"],
                                                                           event_info["dire_team_name"])})
        return event_info

    def get_match_change_history(self):
        return self.match_change_history
