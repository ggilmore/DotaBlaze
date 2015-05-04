__author__ = 'gmgilmore'
import time
import event_types


class Game(object):
    def __init__(self, match_id, *listeners):
        self.id = match_id
        self.game_events = []  # event = (time_stamp, event_type, event_description)
        self.event_listeners = []
        self.event_listeners.extend(*listeners)

        self.last_update_time = time.time()

        self.team_names = ("No Radiant Team Name",
                           "No Dire Team Name")

        self.team_ids = (0, 0)

        self.tower_status = {"radiant": {"top": {"1": True, "2": True, "3": True, "ancient": True},
                                         "middle": {"1": True, "2": True, "3": True},
                                         "bottom": {"1": True, "2": True, "3": True,  "ancient": True},
                                "dire": {"top": {"1": True, "2": True, "3": True,  "ancient": True},
                                         "middle": {"1": True, "2": True, "3": True},
                                         "bottom": {"1": True, "2": True, "3": True, "ancient": True}}}}

        self.barracks_status = {"radiant": {"top": {"melee": True, "ranged": True},
                                            "middle": {"melee": True, "ranged": True},
                                            "bottom": {"melee": True, "ranged": True}},
                                "dire": {"top": {"melee": True, "ranged": True},
                                        "middle": {"melee": True, "ranged": True},
                                        "bottom": {"melee": True, "ranged": True}}}

        self.roshan_timer_status = 0  # 0 = is alive, else is dead

        self.game_timer = 0

        self.kill_count = ({"radiant": 0, "dire": 0}, {"radiant": 0, "dire": 0}, {"radiant": 0, "dire": 0})

    def get_game_events(self):
        return self.game_events

    def get_team_names(self):
        return self.team_names

    def set_team_names(self, names):
        self.team_names = names

    def get_team_ids(self):
        return self.team_ids

    def set_team_ids(self, ids):
        self.team_ids = ids

    def add_event_listener(self, listener):
        self.event_listeners.append(listener)

    def update_game_status(self, info):
        self.last_update_time = time.time()

        new_tower_status = info["tower_status"]
        new_barracks_status = info["barrack_status"]
        new_kill_count = info["kill_count"]
        new_game_timer = info["game_timer"]
        new_rosh_status = info["rosh_status"]

        self.update_tower_status(new_tower_status)
        self.update_barracks_status(new_barracks_status)
        self.update_kill_count(new_kill_count)
        self.update_game_timer(new_game_timer)
        self.update_roshan_timer(new_rosh_status)

    def update_tower_status(self, new_status):
        for side in new_status:
            for location in side[1]:
                for tier in location[1]:
                    if self.tower_status[side[0]][location[0]][tier[0]] != new_status[side[0]][location[0]][tier[0]]:
                        radiant_string = self.team_names[0] + " (Radiant)"
                        dire_string = self.team_names[1] + " (Dire)"

                        tower_killer = radiant_string if side[0] != "radiant" else dire_string
                        tower_loser = radiant_string if tower_killer != "radiant" else dire_string
                        tower_information = location[0] + " tier " + tier[0]

                        info = {"tower_killer": tower_killer, "tower_loser": tower_loser,
                                "tower_information": tower_information}

                        killer_description = event_types.generate_description(event_types.EventType.DESTROYED_TOWER,
                                                                              info)
                        loser_description = event_types.generate_description(event_types.EventType.LOST_TOWER, info)

                        for listener in self.event_listeners:
                            if tower_killer == radiant_string:
                                listener.send_event(self.last_update_time, self.team_ids[0],
                                                    event_types.EventType.DESTROYED_TOWER, killer_description)
                                listener.send_event(self.last_update_time, self.team_ids[1],
                                                    event_types.EventType.LOST_TOWER, loser_description)
                            else:
                                listener.send_event(self.last_update_time, self.team_ids[1],
                                                    event_types.EventType.DESTROYED_TOWER, killer_description)
                                listener.send_event(self.last_update_time, self.team_ids[0],
                                                    event_types.EventType.LOST_TOWER, loser_description)

                        self.game_events.append((self.last_update_time, event_types.EventType.DESTROYED_TOWER,
                                                 killer_description))

                        self.tower_status[side[0]][location[0]][tier[0]] = new_status[side[0]][location[0]][tier[0]]

    def get_formatted_tower_status(self):
        d = self.tower_status
        formatted_dict = {"Radiant": [("Top Tier 1", d["radiant"]["top"]["1"]),
                                      ("Top Tier 2", d["radiant"]["top"]["2"]),
                                      ("Top Tier 3", d["radiant"]["top"]["3"]),
                                      ("Top Tier 4", d["radiant"]["top"]["ancient"]),
                                      ("Middle Tier 1", d["radiant"]["middle"]["1"]),
                                      ("Middle Tier 2", d["radiant"]["middle"]["2"]),
                                      ("Middle Tier 3", d["radiant"]["middle"]["3"]),
                                      ("Bottom Tier 1", d["radiant"]["top"]["1"]),
                                      ("Bottom Tier 2", d["radiant"]["top"]["2"]),
                                      ("Bottom Tier 3", d["radiant"]["top"]["3"]),
                                      ("Bottom Tier 4", d["radiant"]["top"]["ancient"])],
                          "Dire":    [("Top Tier 1", d["dire"]["top"]["1"]),
                                      ("Top Tier 2", d["dire"]["top"]["2"]),
                                      ("Top Tier 3", d["dire"]["top"]["3"]),
                                      ("Top Tier 4", d["dire"]["top"]["ancient"]),
                                      ("Middle Tier 1", d["dire"]["middle"]["1"]),
                                      ("Middle Tier 2", d["dire"]["middle"]["2"]),
                                      ("Middle Tier 3", d["dire"]["middle"]["3"]),
                                      ("Bottom Tier 1", d["dire"]["top"]["1"]),
                                      ("Bottom Tier 2", d["dire"]["top"]["2"]),
                                      ("Bottom Tier 3", d["dire"]["top"]["3"]),
                                      ("Bottom Tier 4", d["dire"]["top"]["ancient"])]}
        return formatted_dict

    def update_barracks_status(self, new_status):
        for side in new_status:
            for location in side[1]:
                for type in location[1]:
                    if self.barracks_status[side[0]][location[0]][type[0]] != new_status[side[0]][location[0]][type[0]]:

                        radiant_string = self.team_names[0] + " (Radiant)"
                        dire_string = self.team_names[1] + " (Dire)"

                        barracks_killer = radiant_string if side[0] != "radiant" else dire_string
                        barracks_loser = radiant_string if barracks_killer != "radiant" else dire_string
                        barracks_information = location[0] + " " + type[0]

                        info = {"barracks_killer": barracks_killer, "barracks_loser": barracks_loser,
                                "barracks_information": barracks_information}

                        killer_description = event_types.generate_description(event_types.EventType.DESTROYED_BARRACKS,
                                                                              info)

                        loser_description = event_types.generate_description(event_types.EventType.LOST_BARRACKS, info)

                        for listener in self.event_listeners:
                            if barracks_killer == radiant_string:
                                listener.send_event(self.last_update_time, self.team_ids[0],
                                                    event_types.EventType.DESTROYED_BARRACKS, killer_description)
                                listener.send_event(self.last_update_time, self.team_ids[1],
                                                    event_types.EventType.LOST_BARRACKS, loser_description)
                            else:
                                listener.send_event(self.last_update_time, self.team_ids[1],
                                                    event_types.EventType.DESTROYED_BARRACKS, killer_description)
                                listener.send_event(self.last_update_time, self.team_ids[0],
                                                    event_types.EventType.LOST_BARRACKS, loser_description)

                        self.game_events.append((self.last_update_time, event_types.EventType.DESTROYED_BARRACKS,
                                                 killer_description))

                        self.barracks_status[side[0]][location[0]][type[0]] = new_status[side[0]][location[0]][type[0]]

    def update_kill_count(self, new_count):
        old_count = self.kill_count
        self.kill_count = (new_count, old_count[0], old_count[1])
        # TODO: add checking for ultra kills and listener notification

    def update_game_timer(self, new_game_timer):
        self.game_timer = new_game_timer
        # TODO: What do we want to do with this?

    def update_roshan_timer(self, new_roshan_timer):
        old_timer = self.roshan_timer_status
        self.roshan_timer_status = new_roshan_timer
        if old_timer == 0 and self.roshan_timer_status > 0:
            for listener in self.event_listeners:
                listener.send_event(event_types.EventType.ROSHAN_KILLED, {})
        self.game_events.append((self.last_update_time, event_types.EventType.ROSHAN_KILLED, {}))

        # TODO: figure out how to identify who killed Roshan (look at player inventories?)


