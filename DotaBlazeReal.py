from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route('/dota2')
def index():
    r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v0001/?key=12B9C2C08AAC635D3A305D7D26793738")
    return render_template("index.html", games=processResponse(r.json()[u"result"][u"games"]))


def processResponse(arr):
    processedResponse = map(getMatchInfo, arr)
    return processedResponse

def getTeamName(isRadiant, dotaSideObj):
    if (isRadiant):
        result = dotaSideObj.get(u"radiant_team",{})
    else:
        result = dotaSideObj.get(u"dire_team",{})
    return result.get(u"team_name", u"No Team Name")


def getMatchInfo(game):
    # return (game[u"match_id"], game[u"dire_team"][u"team_name"], game[u"radiant_team"][u"team_name"])
    return {u"match_id": game[u"match_id"], u"radiant": getTeamName(True, game), u"dire": getTeamName(False, game)}


if __name__ == '__main__':
    app.run()

