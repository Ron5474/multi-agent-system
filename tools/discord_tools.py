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

_COLORS = {
    "morning-brief": 0xF4A261,
    "school": 0x4A90D9,
    "research": 0x7B68EE,
    "system": 0x2ECC71,
    "general": 0xFFFFFF,
    "tasks": 0xE74C3C,
}


def post_to_discord(channel: str, message: str, title: str = "") -> str:
    webhook_url = _WEBHOOKS.get(channel)
    if not webhook_url:
        return f"No webhook configured for #{channel}"

    if title:
        # send as embed — supports up to 4096 chars in description
        embeds = []
        # split message into 4096-char chunks if needed
        chunks = [message[i:i+4096] for i in range(0, len(message), 4096)]
        for i, chunk in enumerate(chunks):
            embeds.append({
                "title": title if i == 0 else "",
                "description": chunk,
                "color": _COLORS.get(channel, 0xFFFFFF),
            })
        payload = {"embeds": embeds[:10]}
    else:
        # plain text, chunked across multiple messages
        chunks = [message[i:i+2000] for i in range(0, len(message), 2000)]
        for chunk in chunks:
            requests.post(webhook_url, json={"content": chunk})
        return f"Posted to #{channel}"

    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        return f"Posted to #{channel}"
    return f"Failed to post to #{channel}: HTTP {response.status_code}"
