# tests/test_memory.py
import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def tmp_memory(tmp_path, monkeypatch):
    monkeypatch.setattr("tools.memory.MEMORY_DIR", tmp_path)
    monkeypatch.setattr("tools.memory._METADATA_FILE", tmp_path / "_metadata.json")
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


def test_write_memory_stamps_metadata():
    from tools.memory import write_memory
    import json
    from pathlib import Path
    write_memory("profile/identity.md", "I am Ron")
    metadata_file = Path("memory/_metadata.json")
    # metadata is written to tmp_path/_metadata.json via monkeypatch
    from tools.memory import _METADATA_FILE
    assert _METADATA_FILE.exists()
    metadata = json.loads(_METADATA_FILE.read_text())
    assert "profile/identity.md" in metadata


def test_check_stale_memory_flags_old_files():
    from tools.memory import write_memory, check_stale_memory, _METADATA_FILE
    import json
    from datetime import datetime, timezone, timedelta
    write_memory("profile/identity.md", "I am Ron")
    # backdate the timestamp to 100 days ago
    metadata = json.loads(_METADATA_FILE.read_text())
    metadata["profile/identity.md"] = (datetime.now(timezone.utc) - timedelta(days=100)).isoformat()
    _METADATA_FILE.write_text(json.dumps(metadata))
    result = check_stale_memory(days=90)
    assert "profile/identity.md" in result
    assert "100 days ago" in result


def test_check_stale_memory_all_fresh():
    from tools.memory import write_memory, check_stale_memory
    write_memory("profile/identity.md", "I am Ron")
    result = check_stale_memory(days=90)
    assert "All memory files" in result


def test_append_log_creates_and_appends():
    from tools.memory import append_log, read_memory
    append_log("Agent started")
    append_log("Task completed")
    log = read_memory("daily_log.md")
    assert "Agent started" in log
    assert "Task completed" in log
