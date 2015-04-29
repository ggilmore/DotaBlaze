__author__ = 'gmgilmore'

from enum import Enum
class EventType(Enum):
    MATCH_STARTED = 1
    MATCH_ENDED = 2
    DESTROYED_TOWER = 3
    DESTROYED_BARRACKS = 4
    ROSHAN_KILLED = 5
    GAME_OVER = 6
    TEAM_NOT_FOUND = 7
    LOST_TOWER = 8
    LOST_BARRACKS = 9

def generate_description(event_type, event_information):
    if event_type == EventType.MATCH_STARTED:
        return "The match between " + event_information["radiant_team"] + \
               " and " + event_information["dire_team"] + " is starting now!"
    elif event_type == EventType.MATCH_ENDED:
        return "The match between " + event_information["radiant_team"] + " and " \
               + event_information["dire_team"] + " just ended!"
    elif event_type == EventType.DESTROYED_TOWER:
        return event_information["tower_killer"] + " just destroyed " + event_information["tower_loser"]+"'s " + \
            event_information["tower_information"] + " tower!"
    elif event_information == EventType.LOST_TOWER:
        return event_information["tower_loser"] + " just lost their " +  event_information["tower_information"] + \
            "against" + event_information["tower_killer"]+"!"

    elif event_type == EventType.DESTROYED_BARRACKS:
        return event_information["barracks_killer"] + " just destroyed " + event_information["barracks_loser"]+"'s " + \
            event_information["barracks_information"] + " barracks!"

    elif event_type == EventType.LOST_BARRACKS:
        return event_information["barracks_loser"] + " just lost their " + event_information["barracks_information"] + \
            "barracks against " + event_information["barracks_killer"]+"!"

    elif event_type == EventType.ROSHAN_KILLED:
        return "Roshan has been killed!"

    elif event_type == EventType.GAME_OVER:
        return "The game with event id: " + str(event_information["id"]) + " is not being played currently."
    elif event_type == EventType.TEAM_NOT_FOUND:
        return "I have not seen a game from the team with id: " + str(event_information["team_id"]) + " yet."

    else:
        return "Whoops!"



