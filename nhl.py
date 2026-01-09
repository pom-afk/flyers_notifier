import requests
from datetime import datetime, timezone

API_BASE = "https://api-web.nhle.com/v1"

def get_todays_game(team_id):
    resp = requests.get(f"{API_BASE}/schedule/now").json()
    today = datetime.now().date().isoformat()
    for day in resp["gameWeek"]:
        if day["date"] == today:
            for game in day["games"]:
                if game["homeTeam"]["id"] == team_id or game["awayTeam"]["id"] == team_id:
                    game["start"] = datetime.fromisoformat(game["startTime"].replace("Z", "+00:00"))
                    return game
    return None

def get_game_state(game_pk):
    resp = requests.get(f"{API_BASE}/game/{game_pk}/feed/live").json()
    # Simplified example: returns next period start time
    # Replace with real logic if you want
    next_start = None
    try:
        next_start_iso = resp["liveData"]["linescore"]["currentPeriodEndTime"]
        if next_start_iso:
            next_start = datetime.fromisoformat(next_start_iso.replace("Z", "+00:00"))
    except:
        pass
    return {"next_start": next_start}
