from datetime import datetime, timezone, timedelta
from config import TEAM_ID, PRE_GAME_MINUTES
from nhl import get_todays_game, get_game_state
from notify import notify
import time

def main():
    game = get_todays_game(TEAM_ID)
    if not game:
        return

    game_pk = game["gamePk"]
    start = game["start"]

    pregame_sent = False
    warned_next = False

    while True:
        now = datetime.now(timezone.utc)

        # Pre-game alert
        if not pregame_sent and now >= start - timedelta(minutes=PRE_GAME_MINUTES):
            notify(f"Flyers game starts in {PRE_GAME_MINUTES} minutes 🏒")
            pregame_sent = True

        # Intermission / next period alert
        state = get_game_state(game_pk)
        if state["next_start"]:
            warn_time = state["next_start"] - timedelta(seconds=60)
            if now >= warn_time and not warned_next:
                notify("Flyers period starting in 1 minute ⏱️")
                warned_next = True
        else:
            warned_next = False

        # Always sleep
        time.sleep(30)

if __name__ == "__main__":
    main()
