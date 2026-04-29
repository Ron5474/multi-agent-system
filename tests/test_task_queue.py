# tests/test_task_queue.py
import json
import pytest
from pathlib import Path
from unittest.mock import patch


@pytest.fixture(autouse=True)
def tmp_tasks(tmp_path, monkeypatch):
    tasks_file = tmp_path / "tasks.json"
    monkeypatch.setattr("core.task_queue.TASKS_FILE", tasks_file)
    return tasks_file


def test_add_task_creates_file():
    from core.task_queue import add_task
    task = add_task("research", "summarize diffusion models")
    assert task["type"] == "research"
    assert task["payload"] == "summarize diffusion models"
    assert task["status"] == "pending"
    assert "id" in task


def test_get_pending_filters_by_type():
    from core.task_queue import add_task, get_pending
    add_task("research", "task A")
    add_task("school", "task B")
    add_task("research", "task C")
    results = get_pending("research")
    assert len(results) == 2
    assert all(t["type"] == "research" for t in results)


def test_update_status_changes_status():
    from core.task_queue import add_task, update_status, get_pending
    task = add_task("research", "task A")
    update_status(task["id"], "in_progress")
    pending = get_pending("research")
    assert len(pending) == 0


def test_list_tasks_returns_all_when_no_filter():
    from core.task_queue import add_task, list_tasks
    add_task("research", "A")
    add_task("school", "B")
    assert len(list_tasks()) == 2


def test_list_tasks_filters_by_type():
    from core.task_queue import add_task, list_tasks
    add_task("research", "A")
    add_task("school", "B")
    assert len(list_tasks("research")) == 1


def test_remove_task_deletes_by_id():
    from core.task_queue import add_task, remove_task, list_tasks
    task = add_task("research", "A")
    add_task("research", "B")
    result = remove_task(task["id"])
    assert "removed" in result
    assert len(list_tasks()) == 1


def test_remove_task_returns_error_for_missing_id():
    from core.task_queue import remove_task
    result = remove_task("nonexistent-id")
    assert "No task found" in result
