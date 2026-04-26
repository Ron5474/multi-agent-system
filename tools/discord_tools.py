import os
import requests
from dotenv import load_dotenv

load_dotenv()

_WEBHOOKS = {
    "general": os.getenv("DISCORD_WEBHOOK_GENERAL"),
    "morning-brief": os.getenv("DISCORD_WEBHOOK_MORNING_BRIEF"),
    "school": os.getenv("DISCORD_WEBHOOK_SCHOOL"),
    "research": os.getenv("DISCORD_WEBHOOK_RESEARCH"),
    "system": os.getenv("DISCORD_WEBHOOK_SYSTEM"),
    "tasks": os.getenv("DISCORD_WEBHOOK_TASKS"),
}


def post_to_discord(channel: str, message: str) -> str:
    webhook_url = _WEBHOOKS.get(channel)
    if not webhook_url:
        return f"No webhook configured for #{channel}"
    response = requests.post(webhook_url, json={"content": message[:2000]})
    if response.status_code == 204:
        return f"Posted to #{channel}"
    return f"Failed to post to #{channel}: HTTP {response.status_code}"
