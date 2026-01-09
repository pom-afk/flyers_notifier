import requests
from datetime import datetime, timezone

API_BASE = "https://api-web.nhle.com/v1"

def get_todays_game(team_id):
    """
    Returns today's game for the given team_id, or None if no game today.
    Adds a 'start' datetime field to the game dict.
    """
    try:
        resp = requests.get(f"{API_BASE}/schedule/now").json()
    except Exception as e:
        print("Error fetching schedule:", e)
        return None

    today = datetime.now().date().isoformat()

    # Debug: print the raw API response if you need to inspect
    # print(resp)

    for day in resp.get("gameWeek", []):
        if day.get("date") == today:
            for game in day.get("games", []):
                home_id = game.get("homeTeam", {}).get("id")
                away_id = game.get("awayTeam", {}).get("id")
                if team_id in [home_id, away_id]:
                    # Use 'startTime' if it exists, otherwise fallback to 'gameDate'
                    start_str = game.get("startTime") or game.get("gameDate")
                    if start_str:
                        game["start"] = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
                        return game
    return None


def get_game_state(game_pk):
    """
    Returns a simplified game state: the next period start time.
    If there’s no upcoming period, next_start will be None.
    """
    try:
        resp = requests.get(f"{API_BASE}/game/{game_pk}/feed/live").json()
        next_start = None
        try:
            next_start_iso = resp["liveData"]["linescore"]["currentPeriodEndTime"]
            if next_start_iso:
                next_start = datetime.fromisoformat(next_start_iso.replace("Z", "+00:00"))
        except KeyError:
            # If the key doesn't exist, just return None
            pass
        return {"next_start": next_start}
    except Exception as e:
        print("Error fetching game state:", e)
        return {"next_start": None}
