import requests
from config import NTFY_TOPIC

def notify(message: str, title: str = None, icon: str = None, priority: int = 3, 
           click_url: str = None):
    """
    Sends a notification to the configured ntfy topic.
    Supports optional title, icon, priority, and click URL.
    """
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    headers = {
        "Priority": str(priority)
    }
    if title:
        headers["Title"] = title
    if icon:
        headers["Icon"] = icon
    if click_url:
        headers["Click"] = click_url

    try:
        resp = requests.post(url, data=message.encode('utf-8'), headers=headers)
        resp.raise_for_status()
        print(f"Notification sent: {message}")
    except Exception as e:
        print(f"Failed to send notification: {e}")
