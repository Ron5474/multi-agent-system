import pytest
from datetime import datetime, timezone, timedelta


@pytest.fixture(autouse=True)
def tmp_buffer(tmp_path, monkeypatch):
    monkeypatch.setattr("core.conversation_buffer._BUFFER_FILE", tmp_path / "conversation_buffer.json")


def test_load_empty_buffer():
    from core.conversation_buffer import load_buffer
    assert load_buffer() == []


def test_save_and_load_exchange():
    from core.conversation_buffer import save_exchange, load_buffer
    save_exchange("hello", "hi there")
    buffer = load_buffer()
    assert buffer[0] == {"role": "user", "content": "hello"}
    assert buffer[1] == {"role": "assistant", "content": "hi there"}


def test_buffer_capped_at_max_exchanges():
    from core.conversation_buffer import save_exchange, load_buffer
    for i in range(7):
        save_exchange(f"message {i}", f"reply {i}")
    buffer = load_buffer()
    assert len(buffer) == 10
    assert buffer[0]["content"] == "message 2"


def test_buffer_expires_after_2_hours():
    from core.conversation_buffer import save_exchange, load_buffer, _BUFFER_FILE
    import json
    save_exchange("hello", "hi")
    # backdate last_active by 3 hours
    data = json.loads(_BUFFER_FILE.read_text())
    data["last_active"] = (datetime.now(timezone.utc) - timedelta(hours=3)).isoformat()
    _BUFFER_FILE.write_text(json.dumps(data))
    assert load_buffer() == []


def test_buffer_still_valid_within_2_hours():
    from core.conversation_buffer import save_exchange, load_buffer, _BUFFER_FILE
    import json
    save_exchange("hello", "hi")
    data = json.loads(_BUFFER_FILE.read_text())
    data["last_active"] = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    _BUFFER_FILE.write_text(json.dumps(data))
    assert len(load_buffer()) == 2


def test_clear_buffer():
    from core.conversation_buffer import save_exchange, clear_buffer, load_buffer
    save_exchange("hello", "hi")
    clear_buffer()
    assert load_buffer() == []
