import pytest
from datetime import datetime, timezone, timedelta


@pytest.fixture(autouse=True)
def tmp_deadlines(tmp_path, monkeypatch):
    monkeypatch.setattr("tools.custom_deadlines._DEADLINES_FILE", tmp_path / "custom_deadlines.json")


def test_add_and_list_deadline():
    from tools.custom_deadlines import add_deadline, list_deadlines
    add_deadline("Midterm Exam", "2026-05-15", "CMPE-297")
    deadlines = list_deadlines()
    assert len(deadlines) == 1
    assert deadlines[0]["name"] == "Midterm Exam"
    assert deadlines[0]["course"] == "CMPE-297"


def test_add_deadline_invalid_date():
    from tools.custom_deadlines import add_deadline
    result = add_deadline("Bad Date", "May 15")
    assert "Invalid date" in result


def test_remove_deadline():
    from tools.custom_deadlines import add_deadline, remove_deadline, list_deadlines
    add_deadline("Exam", "2026-05-20")
    deadline_id = list_deadlines()[0]["id"]
    result = remove_deadline(deadline_id)
    assert "removed" in result
    assert len(list_deadlines()) == 0


def test_remove_deadline_missing_id():
    from tools.custom_deadlines import remove_deadline
    result = remove_deadline("nonexistent")
    assert "No deadline found" in result


def test_get_upcoming_custom_filters_by_date():
    from tools.custom_deadlines import add_deadline, get_upcoming_custom
    future = (datetime.now(timezone.utc) + timedelta(days=5)).strftime("%Y-%m-%d")
    far_future = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
    add_deadline("Soon Exam", future, "CMPE-259")
    add_deadline("Far Exam", far_future, "CMPE-259")
    upcoming = get_upcoming_custom(days=14)
    assert len(upcoming) == 1
    assert upcoming[0]["name"] == "Soon Exam"
