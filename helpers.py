__author__ = 'gmgilmore'
from tower_status_tracker import tower_status, barracks_status


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
    dictionary = {
        u"match_id": game[u"match_id"],
        u"radiant": get_team_name(True, game),
        u"dire": get_team_name(False, game),
        u"dire_tower_status": {},
        u"dire_barracks_status": {},
        u"radiant_tower_status": {},
        u"radiant_barracks_status": {},
        u"duration": {},
        u"roshan_respawn_timer": {},
        u"radiant_kill_count": {},
        u"dire_kill_count": {},
        }
    if u"scoreboard" in game.keys():
        dictionary.update({
            u"dire_tower_status": tower_status(False, bin(game[u"scoreboard"][u"dire"][u"tower_state"])),
            u"dire_barracks_status": barracks_status(False, bin(game[u"scoreboard"][u"dire"][u"barracks_state"])),
            u"radiant_tower_status": tower_status(True, bin(game[u"scoreboard"][u"radiant"][u"tower_state"])),
            u"radiant_barracks_status": barracks_status(False, bin(game[u"scoreboard"][u"radiant"][u"barracks_state"])),
            u"duration": game.get(u"duration", 0),
            u"roshan_respawn_timer": game.get(u"roshan_respawn_timer", 0),
            u"radiant_kill_count": game[u"scoreboard"][u"radiant"][u"score"],
            u"dire_kill_count": game[u"scoreboard"][u"dire"][u"score"],
            })
    return dictionary
