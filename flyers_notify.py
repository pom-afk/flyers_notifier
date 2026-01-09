import os
from ntfy import Client

TOPIC = os.environ.get("NTFY_TOPIC", "flyers-notifier")

client = Client(topic=TOPIC)

def notify(message):
    client.publish(message)
