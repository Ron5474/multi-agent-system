import os
from datetime import datetime, timezone, timedelta
import requests
from icalendar import Calendar
from dotenv import load_dotenv

load_dotenv()

_ICAL_URL = os.getenv("CANVAS_ICAL_URL")


def get_upcoming_assignments(days: int = 14) -> str:
    if not _ICAL_URL:
        return "CANVAS_ICAL_URL not set in .env"

    resp = requests.get(_ICAL_URL, timeout=10)
    if resp.status_code != 200:
        return f"Failed to fetch iCal feed: HTTP {resp.status_code}"

    cal = Calendar.from_ical(resp.content)
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    cutoff = today_start + timedelta(days=days)
    upcoming = []

    for component in cal.walk():
        if component.name != "VEVENT":
            continue
        due = component.get("DTSTART")
        if not due:
            continue
        due_dt = due.dt
        if not hasattr(due_dt, "tzinfo"):
            due_dt = datetime(due_dt.year, due_dt.month, due_dt.day, tzinfo=timezone.utc)
        if due_dt.tzinfo is None:
            due_dt = due_dt.replace(tzinfo=timezone.utc)
        if not (today_start <= due_dt <= cutoff):
            continue

        summary = str(component.get("SUMMARY", "Untitled"))
        delta = (due_dt - today_start).days
        upcoming.append({
            "name": summary,
            "due_at": due_dt.strftime("%b %d %I:%M %p"),
            "days_left": delta,
            "due_dt": due_dt,
        })

    if not upcoming:
        return f"No assignments due in the next {days} days."

    upcoming.sort(key=lambda x: x["days_left"])
    lines = []
    for a in upcoming:
        if a["days_left"] == 0:
            time_str = "today"
        elif a["days_left"] == 1:
            time_str = "tomorrow"
        else:
            time_str = f"{a['days_left']}d"
        lines.append(f"- {a['name']} — due {a['due_at']} ({time_str})")
    return "\n".join(lines)
