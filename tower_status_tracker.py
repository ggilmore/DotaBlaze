__author__ = 'gmgilmore'

ANCIENT_INDEX = 2
BOTTOM_INDEX = 5
MIDDLE_INDEX = 8
TOP_INDEX = 11

DIRE_INDEX = 11


def get_side_string(is_radiant):
    if is_radiant:
        return "radiant"
    else:
        return "dire"


def tower_status(is_radiant, tower_status_string_raw):
    side_tower_bit_string_length = 13
    if len(tower_status_string_raw) == side_tower_bit_string_length:
        tower_status_string = tower_status_string_raw[2:]

        ancient_bits = tower_status_string[:ANCIENT_INDEX]
        bottom_bits = tower_status_string[ANCIENT_INDEX:BOTTOM_INDEX]
        middle_bits = tower_status_string[BOTTOM_INDEX:MIDDLE_INDEX]
        top_bits = tower_status_string[MIDDLE_INDEX:TOP_INDEX]

        ancient_dict = tower_status_helper("ancient", True, ancient_bits)
        bottom_dict = tower_status_helper("bottom", False, bottom_bits)
        middle_dict = tower_status_helper("middle", False, middle_bits)
        top_dict = tower_status_helper("top", False, top_bits)

        side_string = get_side_string(is_radiant)
        return_dict = {side_string: {}}

        # add all lane dicts together
        for lane_dict in [top_dict, middle_dict, bottom_dict]:
            return_dict[side_string].update(lane_dict)

        # add ancients in proper lanes
        return_dict[side_string]["top"].update(ancient_dict["top"])
        return_dict[side_string]["bottom"].update(ancient_dict["bottom"])

        return return_dict
    else:
        return {}


def tower_status_helper(location_string, is_ancient, tower_status_string):
    if not is_ancient:
        assert len(tower_status_string) == 3
        tier3 = tower_status_string[0] == u"1"
        tier2 = tower_status_string[1] == u"1"
        tier1 = tower_status_string[2] == u"1"
        return {location_string: {"1": tier1, "2": tier2, "3": tier3}}
    else:
        assert len(tower_status_string) == 2
        top = tower_status_string[0] == u"1"
        bot = tower_status_string[1] == u"1"
        return {"top": {location_string: top}, "bottom": {location_string: bot}}
