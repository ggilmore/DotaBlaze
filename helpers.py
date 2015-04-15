__author__ = 'gmgilmore'
from tower_status_tracker import tower_status


def process_response(arr):
    processed_response = map(get_match_info, arr)
    return processed_response


def get_team_name(is_radiant, dota_side_obj):
    if (is_radiant):
        result = dota_side_obj.get(u"radiant_team",{})
    else:
        result = dota_side_obj.get(u"dire_team",{})
    return result.get(u"team_name", u"No Team Name")


def get_match_info(game):
    if u"scoreboard" in game.keys():
        dictionary =  {u"match_id": game[u"match_id"],
                u"radiant": get_team_name(True, game),
                u"dire": get_team_name(False, game),
                u"dire_tower_status": tower_status(False, bin(game[u"scoreboard"][u"dire"][u"tower_state"])),
                u"radiant_tower_status": tower_status(True, bin(game[u"scoreboard"][u"radiant"][u"tower_state"]))}
    else:
        dictionary =  {u"match_id": game[u"match_id"],
                u"radiant": get_team_name(True, game),
                u"dire": get_team_name(False, game),
                u"dire_tower_status": {u"Towers": u"Unknown"},
                u"radiant_tower_status": {u"Towers": u"Unknown"}}
    return dictionary
