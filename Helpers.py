__author__ = 'gmgilmore'
from TowerStatusTracker import towerStatus

def processResponse(arr):
    processedResponse = map(getMatchInfo, arr)
    print processedResponse
    return processedResponse

def getTeamName(isRadiant, dotaSideObj):
    if (isRadiant):
        result = dotaSideObj.get(u"radiant_team",{})
    else:
        result = dotaSideObj.get(u"dire_team",{})
    return result.get(u"team_name", u"No Team Name")


def getMatchInfo(game):
    # return (game[u"match_id"], game[u"dire_team"][u"team_name"], game[u"radiant_team"][u"team_name"])

    if u"scoreboard" in game.keys():
        dictionary =  {u"match_id": game[u"match_id"],
                u"radiant": getTeamName(True, game),
                u"dire": getTeamName(False, game),
                u"dire_tower_status": towerStatus(False, bin(game[u"scoreboard"][u"dire"][u"tower_state"])),
                u"radiant_tower_status": towerStatus(True, bin(game[u"scoreboard"][u"radiant"][u"tower_state"]))}
    else:
        dictionary =  {u"match_id": game[u"match_id"],
                u"radiant": getTeamName(True, game),
                u"dire": getTeamName(False, game),
                u"dire_tower_status": {u"Towers": u"Unknown"},
                u"radiant_tower_status": {u"Towers": u"Unknown"}}
    return dictionary