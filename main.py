from datetime import datetime, timezone, timedelta
from nhl import get_todays_game, get_game_state
from notify import notify
import time
import os

TEAM_ID = int(os.environ.get("TEAM_ID", 4))
PRE_GAME_MINUTES = 30

def main():
    notify("Flyers notifier started 🚨")
    game = get_todays_game(TEAM_ID)
    if not game:
        return

    game_pk = game["gamePk"]
    start = game["start"]

    pregame_sent = False
    warned_next = False

    while True:
        now = datetime.now(timezone.utc)

        # Notify 30 min before game
        if not pregame_sent and now >= start - timedelta(minutes=PRE_GAME_MINUTES):
            notify("Flyers game starts in 30 minutes 🏒")
            pregame_sent = True

        # Check game state
        state = get_game_state(game_pk)
        if state["next_start"]:
            warn_time = state["next_start"] - timedelta(seconds=60)
            if now >= warn_time and not warned_next:
                notify("Flyers period starting in 1 minute ⏱️")
                warned_next = True
        else:
            warned_next = False

        time.sleep(30)

if __name__ == "__main__":
    main()
