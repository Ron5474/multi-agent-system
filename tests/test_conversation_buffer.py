import pytest


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
    # max 5 exchanges = 10 messages
    assert len(buffer) == 10
    # should contain the last 5 exchanges
    assert buffer[0]["content"] == "message 2"


def test_clear_buffer():
    from core.conversation_buffer import save_exchange, clear_buffer, load_buffer
    save_exchange("hello", "hi")
    clear_buffer()
    assert load_buffer() == []
