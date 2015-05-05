__author__ = 'gmgilmore'

ANCIENT_TOWER_INDEX = 2
BOTTOM_TOWER_INDEX = 5
MIDDLE_TOWER_INDEX = 8
TOP_TOWER_INDEX = 11

BOTTOM_BARRACKS_INDEX = 2
MIDDLE_BARRACKS_INDEX = 4
TOP_BARRACKS_INDEX = 6


def get_side_string(is_radiant):
    if is_radiant:
        return "radiant"
    else:
        return "dire"


def tower_status(is_radiant, tower_status_string_raw):
    # remove the "0b" from the binary string and pad to length of 11
    tower_status_string = tower_status_string_raw[2:].zfill(11)

    ancient_bits = tower_status_string[:ANCIENT_TOWER_INDEX]
    bottom_bits = tower_status_string[ANCIENT_TOWER_INDEX:BOTTOM_TOWER_INDEX]
    middle_bits = tower_status_string[BOTTOM_TOWER_INDEX:MIDDLE_TOWER_INDEX]
    top_bits = tower_status_string[MIDDLE_TOWER_INDEX:TOP_TOWER_INDEX]

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


def barracks_status(is_radiant, barrack_status_string_raw):
    # remove the "0b" from the binary string and pad to length of 6
    barrack_status_string = barrack_status_string_raw[2:].zfill(6)

    top_bits = barrack_status_string[MIDDLE_BARRACKS_INDEX:TOP_BARRACKS_INDEX]
    middle_bits = barrack_status_string[BOTTOM_BARRACKS_INDEX:MIDDLE_BARRACKS_INDEX]
    bottom_bits = barrack_status_string[:BOTTOM_BARRACKS_INDEX]

    return {get_side_string(is_radiant):
                {"top": barracks_status_helper(top_bits),
                "middle": barracks_status_helper(middle_bits),
                "bottom": barracks_status_helper(bottom_bits)}}


def barracks_status_helper(barracks_status_string):
    assert len(barracks_status_string) == 2
    melee_status = barracks_status_string[0] == u"1"
    ranged_status = barracks_status_string[1] == u"2"
    return {"melee": melee_status, "ranged": ranged_status}
