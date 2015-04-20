__author__ = 'gmgilmore'
import time
import event_types

class Game:
    def __init__(self, id, radiant_team_name, dire_team_name, *listeners):
        self.id = id

        self.event_listeners = []
        self.event_listeners.extend(*listeners)

        self.last_update_time = time.time()

        self.team_names = (radiant_team_name, dire_team_name)

        self.tower_status = {"radiant": {"top": {"1": True, "2": True, "3": True, "ancient": True},
                                         "middle": {"1": True, "2": True, "3": True},
                                         "bottom": {"1": True, "2": True, "3": True},  "ancient":True},
                                "dire": {"top": {"1": True, "2": True, "3": True,  "ancient":True},
                                        "middle": {"1": True, "2": True, "3": True},
                                        "bottom": {"1": True, "2": True, "3": True, "ancient": True}}}

        self.barracks_status = {"radiant": {"top": {"melee": True, "ranged": True,},
                                            "middle": {"melee": True, "ranged": True},
                                            "bottom": {"melee": True, "ranged": True}},
                                "dire": {"top": {"melee": True, "ranged": True},
                                        "middle": {"melee": True, "ranged": True},
                                        "bottom": {"melee": True, "ranged": True}}}

        self.roshan_timer_status = 0 # 0 = is alive, else is dead

        self.game_timer = 0

        self.kill_count = ({"radiant": 0, "dire": 0}, {"radiant": 0, "dire": 0}, {"radiant": 0, "dire": 0})

    def update_game_status(self, info):
        self.last_update_time = time.time()

    def update_tower_status(self, new_status):
        for side in new_status:
            for location in side[1]:
                for tier in location[1]:
                    if self.tower_status[side[0]][location[0]][tier[0]] != new_status[side[0]][location[0]][tier[0]]:
                        tower_killer = "radiant" if side[0] != "radiant" else "dire"
                        tower_loser = "radiant" if tower_killer != "radiant" else "dire"
                        tower_information = location[0] + " tier " + tier[0]

                        info = {"tower_killer": tower_killer, "tower_loser": tower_loser,
                                "tower_information": tower_information}

                        for listener in self.event_listeners:
                            listener.send_event(event_types.EventType.TOWER_DESTROYED,
                                                event_types.generate_description(event_types.EventType.TOWER_DESTROYED),
                                                info)

                        self.tower_status[side[0]][location[0]][tier[0]] = new_status[side[0]][location[0]][tier[0]]

    def update_barracks_status(self, new_status):
        for side in new_status:
            for location in side[1]:
                for type in location[1]:
                    if self.barracks_status[side[0]][location[0]][type[0]] != new_status[side[0]][location[0]][type[0]]:
                        barracks_killer = "radiant" if side[0] != "radiant" else "dire"
                        barracks_loser = "radiant" if barracks_killer != "radiant" else "dire"
                        barracks_information = location[0] + " " + type[0]

                        info = {"barracks_killer": barracks_killer, "barracks_loser": barracks_loser,
                                "barracks_information": barracks_information}

                        for listener in self.event_listeners:
                            listener.send_event(event_types.EventType.BARRACKS_DESTROYED,
                                                event_types.generate_description(event_types.EventType.BARRACKS_DESTROYED),
                                                info)

                        self.barracks_status[side[0]][location[0]][type[0]] = new_status[side[0]][location[0]][type[0]]

    def update_kill_count(self, new_count):
        old_count = self.kill_count
        self.kill_count = (new_count, old_count[0], old_count[1])
        #TODO: add checking for ultra kills and listener notification


