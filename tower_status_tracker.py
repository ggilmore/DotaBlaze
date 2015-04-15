__author__ = 'gmgilmore'

ANCIENT_INDEX = 2
BOTTOM_INDEX = 5
MIDDLE_INDEX = 8
TOP_INDEX = 11

DIRE_INDEX = 11


def get_side_string(is_radiant):
    if is_radiant:
        side = u"Radiant"
    else:
        side =u"Dire"
    return side


def tower_status(is_radiant, tower_status_string_raw):
    side_tower_bit_string_length = 13
    if len(tower_status_string_raw) == side_tower_bit_string_length:
        tower_status_string = tower_status_string_raw[2:]

        ancient_bits = tower_status_string[:ANCIENT_INDEX]
        bottom_bits = tower_status_string[ANCIENT_INDEX:BOTTOM_INDEX]
        middle_bits = tower_status_string[BOTTOM_INDEX:MIDDLE_INDEX]
        top_bits = tower_status_string[MIDDLE_INDEX:TOP_INDEX]

        ancient_dict = tower_status_helper(u" Ancient", True, ancient_bits)
        bottom_dict = tower_status_helper(u" Bottom", False, bottom_bits)
        middle_dict = tower_status_helper(u" Middle", False, middle_bits)
        top_dict = tower_status_helper(u" Top", False, top_bits)

        side_string = get_side_string(is_radiant)
        tower_status_no_side = []

        for tempList in [top_dict, middle_dict, bottom_dict, ancient_dict]:
            tower_status_no_side.extend(tempList)

        return [(side_string+entry[0], entry[1]) for entry in tower_status_no_side]
    else:
        return []


def tower_status_helper(location_string, is_ancient, tower_status_string):
    if not is_ancient:
        assert len(tower_status_string) == 3
        tier3 = tower_status_string[0] == u"1"
        tier2 = tower_status_string[1] == u"1"
        tier1 = tower_status_string[2] == u"1"
        return [(location_string + u" Tier 3", tier3), (location_string + u" Tier 2", tier2),
                (location_string + u" Tier 1", tier1)]
    else:
        assert len(tower_status_string) == 2
        top = tower_status_string[0] == u"1"
        bot = tower_status_string[1] == u"1"
        return [(location_string + u" Top", top), (location_string + u" Bottom", bot)]
