from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta


def _future(days):
    return (datetime.now(timezone.utc) + timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_get_upcoming_returns_formatted_assignments():
    mock_courses = [{"id": 1, "name": "CS280"}]
    mock_assignments = [
        {"name": "HW3", "due_at": _future(5), "html_url": "https://sjsu.instructure.com/courses/1/assignments/1"},
    ]

    with patch("tools.canvas._TOKEN", "fake-token"), \
         patch("tools.canvas.requests.get") as mock_get:

        def side_effect(url, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            if "courses/1/assignments" in url:
                resp.json.return_value = mock_assignments
            else:
                resp.json.return_value = mock_courses
            return resp

        mock_get.side_effect = side_effect
        from tools.canvas import get_upcoming_assignments
        result = get_upcoming_assignments(days=14)

    assert "CS280" in result
    assert "HW3" in result
    assert "d)" in result  # days remaining present in some form


def test_get_upcoming_returns_message_when_none():
    mock_courses = [{"id": 1, "name": "CS280"}]

    with patch("tools.canvas._TOKEN", "fake-token"), \
         patch("tools.canvas.requests.get") as mock_get:

        def side_effect(url, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            if "assignments" in url:
                resp.json.return_value = []
            else:
                resp.json.return_value = mock_courses
            return resp

        mock_get.side_effect = side_effect
        from tools.canvas import get_upcoming_assignments
        result = get_upcoming_assignments(days=14)

    assert "No assignments" in result


def test_get_upcoming_returns_error_when_no_token():
    with patch("tools.canvas._TOKEN", None):
        from tools.canvas import get_upcoming_assignments
        result = get_upcoming_assignments()
    assert "not set" in result
