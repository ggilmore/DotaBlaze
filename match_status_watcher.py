from Helpers import processResponse

import requests

dota2_url = "https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v0001/?key=12B9C2C08AAC635D3A305D7D26793738"

class MatchTracker(object):

    def __init__(self, url=dota2_url):
        self.url = url
        self.match_ids = self.get_matches()

    def get_match_updates(self):
        old_match_ids = self.match_ids
        self.match_ids = self.get_matches()
        return (
            old_match_ids - self.match_ids,
            self.match_ids - old_match_ids
            )

    def get_matches(self):
        r = requests.get(self.url)
        return {ent[u"match_id"] for ent in r.json()[u"result"][u"games"]}
