import requests
from config import NTFY_TOPIC

def notify(msg):
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=msg.encode("utf-8"),
        timeout=5
    )
