import os

NTFY_TOPIC = os.getenv("NTFY_TOPIC", "flyers-alerts-ky-123")
TEAM_ID = int(os.getenv("TEAM_ID", 4))
PRE_GAME_MINUTES = int(os.getenv("PRE_GAME_MINUTES", 30))
PERIOD_WARNING_SECONDS = int(os.getenv("PERIOD_WARNING_SECONDS", 60))
