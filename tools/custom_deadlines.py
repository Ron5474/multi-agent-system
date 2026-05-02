import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

_DEADLINES_FILE = Path("memory/custom_deadlines.json")


def _load() -> list[dict]:
    if not _DEADLINES_FILE.exists():
        return []
    return json.loads(_DEADLINES_FILE.read_text())


def _save(deadlines: list[dict]) -> None:
    _DEADLINES_FILE.parent.mkdir(exist_ok=True)
    _DEADLINES_FILE.write_text(json.dumps(deadlines, indent=2))


def add_deadline(name: str, due_date: str, course: str = "") -> str:
    """Add a custom deadline. due_date must be YYYY-MM-DD."""
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."
    deadlines = _load()
    entry = {
        "id": str(uuid.uuid4()),
        "name": name,
        "due_date": due_date,
        "course": course,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    deadlines.append(entry)
    _save(deadlines)
    return f"Deadline added: {name} on {due_date}."


def remove_deadline(deadline_id: str) -> str:
    deadlines = _load()
    remaining = [d for d in deadlines if d["id"] != deadline_id]
    if len(remaining) == len(deadlines):
        return f"No deadline found with id {deadline_id}."
    _save(remaining)
    return f"Deadline {deadline_id} removed."


def list_deadlines() -> list[dict]:
    return _load()


def get_upcoming_custom(days: int = 14) -> list[dict]:
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    cutoff = today_start + __import__("datetime").timedelta(days=days)
    upcoming = []
    for d in _load():
        due_dt = datetime.strptime(d["due_date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        if today_start <= due_dt <= cutoff:
            delta = (due_dt - today_start).days
            upcoming.append({
                "name": d["name"],
                "course": d["course"],
                "due_date": d["due_date"],
                "days_left": delta,
                "id": d["id"],
            })
    return upcoming
