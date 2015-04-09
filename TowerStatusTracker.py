__author__ = 'gmgilmore'

ANCIENT_INDEX = 2
BOTTOM_INDEX = 5
MIDDLE_INDEX = 8
TOP_INDEX = 11

DIRE_INDEX = 11



def getSideString(isRadiant):
    if isRadiant:
        side = u"Radiant"
    else:
        side =u"Dire"
    return side

def towerStatus(isRadiant, towerStatusStringRaw):
    sideTowerBitStringLength = 13
    if len(towerStatusStringRaw) == sideTowerBitStringLength:
        towerStatusString = towerStatusStringRaw[2:]

        ancientBits = towerStatusString[:ANCIENT_INDEX]
        bottomBits = towerStatusString[ANCIENT_INDEX:BOTTOM_INDEX]
        middleBits = towerStatusString[BOTTOM_INDEX:MIDDLE_INDEX]
        topBits = towerStatusString[MIDDLE_INDEX:TOP_INDEX]

        ancientDict = towerStatusHelper(u" Ancient", True, ancientBits)
        bottomDict = towerStatusHelper(u" Bottom", False, bottomBits)
        middleDict = towerStatusHelper(u" Middle", False, middleBits)
        topDict = towerStatusHelper(u" Top", False, topBits)

        sideString = getSideString(isRadiant)
        towerStatusNoSide = []

        for tempList in [topDict, middleDict, bottomDict, ancientDict]:
            towerStatusNoSide.extend(tempList)

        return [(sideString+entry[0], entry[1]) for entry in towerStatusNoSide]
    else:
        return []


def towerStatusHelper(locationString, isAncient, towerStatusString):
    if not isAncient:
        assert len(towerStatusString) == 3
        tier3 = towerStatusString[0] == u"1"
        tier2 = towerStatusString[1] == u"1"
        tier1 = towerStatusString[2] == u"1"
        return [(locationString + u" Tier 3", tier3), (locationString + u" Tier 2", tier2),
                (locationString + u" Tier 1", tier1)]
    else:
        assert len(towerStatusString) == 2
        top = towerStatusString[0] == u"1"
        bot = towerStatusString[1] == u"1"
        return [(locationString + u" Top", top), (locationString + u" Bottom", bot)]
