import json
from pathlib import Path

_BUFFER_FILE = Path("memory/conversation_buffer.json")
_MAX_EXCHANGES = 5


def load_buffer() -> list[dict]:
    if not _BUFFER_FILE.exists():
        return []
    return json.loads(_BUFFER_FILE.read_text())


def save_exchange(user_message: str, assistant_reply: str) -> None:
    buffer = load_buffer()
    buffer.append({"role": "user", "content": user_message})
    buffer.append({"role": "assistant", "content": assistant_reply})
    # keep only the last N exchanges (each exchange = 2 messages)
    buffer = buffer[-(_MAX_EXCHANGES * 2):]
    _BUFFER_FILE.parent.mkdir(parents=True, exist_ok=True)
    _BUFFER_FILE.write_text(json.dumps(buffer, indent=2))


def clear_buffer() -> None:
    if _BUFFER_FILE.exists():
        _BUFFER_FILE.write_text("[]")
