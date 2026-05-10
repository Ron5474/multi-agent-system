import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

_BUFFER_FILE = Path("memory/conversation_buffer.json")
_MAX_EXCHANGES = 5
_EXPIRY_HOURS = 2


def _load_raw() -> dict:
    if not _BUFFER_FILE.exists():
        return {"last_active": None, "messages": []}
    return json.loads(_BUFFER_FILE.read_text())


def load_buffer() -> list[dict]:
    data = _load_raw()
    if not data.get("last_active"):
        return []
    last_active = datetime.fromisoformat(data["last_active"])
    if datetime.now(timezone.utc) - last_active > timedelta(hours=_EXPIRY_HOURS):
        clear_buffer()
        return []
    return data.get("messages", [])


def save_exchange(user_message: str, assistant_reply: str) -> None:
    data = _load_raw()
    messages = data.get("messages", [])
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": assistant_reply})
    messages = messages[-(_MAX_EXCHANGES * 2):]
    _BUFFER_FILE.parent.mkdir(parents=True, exist_ok=True)
    _BUFFER_FILE.write_text(json.dumps({
        "last_active": datetime.now(timezone.utc).isoformat(),
        "messages": messages,
    }, indent=2))


def clear_buffer() -> None:
    _BUFFER_FILE.parent.mkdir(parents=True, exist_ok=True)
    _BUFFER_FILE.write_text(json.dumps({"last_active": None, "messages": []}, indent=2))
