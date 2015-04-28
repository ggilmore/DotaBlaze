__author__ = 'gmgilmore'

class EventListener(object):
    def __init__(self):
        self.events = []

    def receive_event(self, event_type, event_dscr):
        self.events.append((event_type, event_dscr))

    def get_all_events(self):
        self.events.copy

