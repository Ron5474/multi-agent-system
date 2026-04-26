# tests/test_memory.py
import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def tmp_memory(tmp_path, monkeypatch):
    monkeypatch.setattr("tools.memory.MEMORY_DIR", tmp_path)
    return tmp_path


def test_write_and_read_memory():
    from tools.memory import write_memory, read_memory
    write_memory("user.md", "I am Ron")
    assert read_memory("user.md") == "I am Ron"


def test_read_missing_file_returns_empty():
    from tools.memory import read_memory
    assert read_memory("missing.md") == ""


def test_write_creates_subdirectory():
    from tools.memory import write_memory, read_memory
    write_memory("research/topic.md", "content")
    assert read_memory("research/topic.md") == "content"


def test_append_log_creates_and_appends():
    from tools.memory import append_log, read_memory
    append_log("Agent started")
    append_log("Task completed")
    log = read_memory("daily_log.md")
    assert "Agent started" in log
    assert "Task completed" in log
