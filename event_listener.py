__author__ = 'gmgilmore'
from event_types import EventType, generate_description

class EventListener(object):
    def __init__(self):
        self.team_events = {}  # dict of teams -> list of event tuples

    def receive_event(self, time_stamp, team_id, event_type, event_dscr):
        event_tuple = (time_stamp, event_type, event_dscr)
        if team_id in self.team_events:
            self.team_events[team_id].append(event_tuple)
        else:
            self.team_events[team_id] = [event_tuple]

    def get_team_events(self, team_id):
        not_found_event = (EventType.TEAM_NOT_FOUND, generate_description(EventType.TEAM_NOT_FOUND,
                                                                          {"team_id": team_id}))
        return self.team_events.get(team_id, not_found_event)



