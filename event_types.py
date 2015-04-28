__author__ = 'gmgilmore'

from enum import Enum
class EventType(Enum):
    MATCH_STARTED = 1
    MATCH_ENDED = 2
    TOWER_DESTROYED = 3
    BARRACKS_DESTROYED = 4
    ROSHAN_KILLED = 5
    GAME_OVER = 6
    TEAM_NOT_FOUND = 7

def generate_description(event_type, event_information):
    if event_type == EventType.MATCH_STARTED:
        return "The match between " + event_information["radiant_team"] + \
               " and " + event_information["dire_team"] + " is starting now!"
    elif event_type == EventType.MATCH_ENDED:
        return "The match between " + event_information["radiant_team"] + " and " \
               + event_information["dire_team"] + " just ended!"
    elif event_type == EventType.TOWER_DESTROYED:
        return event_information["tower_killer"] + " just destroyed " + event_information["tower_loser"]+"'s " + \
            event_information["tower_information"] + " tower!"

    elif event_type == EventType.BARRACKS_DESTROYED:
        return event_information["barracks_killer"] + " just destroyed " + event_information["barracks_loser"]+"'s " + \
            event_information["barracks_information"] + " barracks!"

    elif event_type == EventType.ROSHAN_KILLED:
        return "Roshan has been killed!"

    elif event_type == EventType.GAME_OVER:
        return "The game with event id: " + event_information["id"] + " is not being played currently."
    elif event_type == EventType.TEAM_NOT_FOUND:
        return "I have not seen a game from the team with id: " + str(event_information["team_id"]) + " yet."

    else:
        return "Whoops!"



