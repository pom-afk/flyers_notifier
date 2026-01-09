import requests
from datetime import datetime, timezone
from dateutil import parser

SCHEDULE_URL = "https://api-web.nhle.com/v1/schedule/now"

def get_todays_game(team_id):
    params = {"teamId": team_id}
    data = requests.get(SCHEDULE_URL, params=params, timeout=10).json()

    dates = data.get("dates", [])
    if not dates:
        return None

    game = dates[0]["games"][0]
    start = parser.isoparse(game["gameDate"])

    return {
        "gamePk": game["gamePk"],
        "start": start
    }



LIVE_URL = "https://api-web.nhle.com/v1/gamecenter/{}/play-by-play"


def get_game_state(game_pk):
    data = requests.get(LIVE_URL.format(game_pk), timeout=10).json()

    state = data.get("gameState")
    period = data.get("periodDescriptor", {}).get("number", 0)

    next_start = None
    if state == "INTERMISSION":
        next_start = parser.isoparse(
            data["intermissionInfo"]["endTimeUTC"]
        )

    return {
        "state": state,
        "period": period,
        "next_start": next_start
    }