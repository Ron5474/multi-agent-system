from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta


def _make_ical(summary: str, due_dt: datetime) -> bytes:
    due_str = due_dt.strftime("%Y%m%dT%H%M%SZ")
    return f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:{summary}
DTSTART:{due_str}
END:VEVENT
END:VCALENDAR""".encode()


def test_get_upcoming_returns_formatted_assignments():
    future = datetime.now(timezone.utc) + timedelta(days=5)
    ical_data = _make_ical("CS280 HW3", future)

    with patch("tools.canvas._ICAL_URL", "https://sjsu.instructure.com/feeds/calendars/user_abc.ics"), \
         patch("tools.canvas.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = ical_data
        from tools.canvas import get_upcoming_assignments
        result = get_upcoming_assignments(days=14)

    assert "CS280 HW3" in result
    assert "d)" in result


def test_get_upcoming_returns_message_when_none():
    ical_data = b"""BEGIN:VCALENDAR\nVERSION:2.0\nEND:VCALENDAR"""

    with patch("tools.canvas._ICAL_URL", "https://sjsu.instructure.com/feeds/calendars/user_abc.ics"), \
         patch("tools.canvas.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = ical_data
        from tools.canvas import get_upcoming_assignments
        result = get_upcoming_assignments(days=14)

    assert "No assignments" in result


def test_get_upcoming_includes_already_passed_today():
    # Due at midnight today — should still appear with 0h left
    today_midnight = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    ical_data = _make_ical("CS101 Quiz", today_midnight)

    with patch("tools.canvas._ICAL_URL", "https://sjsu.instructure.com/feeds/calendars/user_abc.ics"), \
         patch("tools.canvas.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = ical_data
        from tools.canvas import get_upcoming_assignments
        result = get_upcoming_assignments(days=14)

    assert "CS101 Quiz" in result
    assert "12:00 AM" in result
    assert "today" in result


def test_get_upcoming_midnight_shows_correct_date():
    future_midnight = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=3)
    ical_data = _make_ical("CS202 Project", future_midnight)

    with patch("tools.canvas._ICAL_URL", "https://sjsu.instructure.com/feeds/calendars/user_abc.ics"), \
         patch("tools.canvas.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = ical_data
        from tools.canvas import get_upcoming_assignments
        result = get_upcoming_assignments(days=14)

    assert "CS202 Project" in result
    assert "12:00 AM" in result
    assert "3d" in result


def test_get_upcoming_returns_error_when_no_url():
    with patch("tools.canvas._ICAL_URL", None):
        from tools.canvas import get_upcoming_assignments
        result = get_upcoming_assignments()
    assert "not set" in result
