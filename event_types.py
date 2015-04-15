__author__ = 'gmgilmore'

from enum import Enum
class EventType(Enum):
    MATCH_STARTED = 1
    MATCH_ENDED = 2

def generate_description(event_type, radiant_team, dire_team):
    if event_type == EventType.MATCH_STARTED:
        return "The match between " + radiant_team + " and " + dire_team + " is starting now!"
    elif event_type == EventType.MATCH_ENDED:
        return "The match between " + radiant_team + " and " + dire_team + " just ended!"
    else:
        return "Whoops!"


{}