import os
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv

load_dotenv()

_BASE_URL = os.getenv("CANVAS_BASE_URL", "https://canvas.sjsu.edu")
_TOKEN = os.getenv("CANVAS_API_TOKEN")


def _headers() -> dict:
    return {"Authorization": f"Bearer {_TOKEN}"}


def get_upcoming_assignments(days: int = 14) -> str:
    if not _TOKEN:
        return "CANVAS_API_TOKEN not set in .env"

    courses_resp = requests.get(
        f"{_BASE_URL}/api/v1/courses",
        headers=_headers(),
        params={"enrollment_state": "active", "per_page": 50},
    )
    if courses_resp.status_code != 200:
        return f"Failed to fetch courses: HTTP {courses_resp.status_code}"

    courses = {c["id"]: c["name"] for c in courses_resp.json() if "name" in c}
    now = datetime.now(timezone.utc)
    upcoming = []

    for course_id, course_name in courses.items():
        assignments_resp = requests.get(
            f"{_BASE_URL}/api/v1/courses/{course_id}/assignments",
            headers=_headers(),
            params={"per_page": 50, "order_by": "due_at"},
        )
        if assignments_resp.status_code != 200:
            continue
        for a in assignments_resp.json():
            due_at = a.get("due_at")
            if not due_at:
                continue
            due = datetime.fromisoformat(due_at.replace("Z", "+00:00"))
            delta = (due - now).days
            if 0 <= delta <= days:
                upcoming.append({
                    "course": course_name,
                    "name": a["name"],
                    "due_at": due.strftime("%b %d %I:%M %p"),
                    "days_left": delta,
                    "url": a.get("html_url", ""),
                })

    if not upcoming:
        return f"No assignments due in the next {days} days."

    upcoming.sort(key=lambda x: x["days_left"])
    lines = [f"- [{a['course']}] {a['name']} — due {a['due_at']} ({a['days_left']}d)" for a in upcoming]
    return "\n".join(lines)
