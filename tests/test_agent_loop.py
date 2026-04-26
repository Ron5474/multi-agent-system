# tests/test_agent_loop.py
import json
from unittest.mock import MagicMock, patch


def _make_message(content=None, tool_calls=None):
    msg = MagicMock()
    msg.content = content
    msg.tool_calls = tool_calls or []
    return msg


def test_returns_plain_text_when_no_tool_calls():
    with patch("core.agent_loop.chat") as mock_chat:
        mock_chat.return_value = _make_message(content="Hello world")
        from core.agent_loop import run
        result = run("you are helpful", "hi", [], {})
    assert result == "Hello world"


def test_executes_tool_and_continues():
    tool_call = MagicMock()
    tool_call.id = "call_123"
    tool_call.function.name = "greet"
    tool_call.function.arguments = json.dumps({"name": "Ron"})

    with patch("core.agent_loop.chat") as mock_chat:
        mock_chat.side_effect = [
            _make_message(content=None, tool_calls=[tool_call]),
            _make_message(content="Done after tool"),
        ]
        from core.agent_loop import run
        result = run(
            "system",
            "user",
            [{"type": "function", "function": {"name": "greet", "parameters": {}}}],
            {"greet": lambda name: f"Hi {name}!"},
        )
    assert result == "Done after tool"
    assert mock_chat.call_count == 2


def test_tool_result_is_appended_to_messages():
    tool_call = MagicMock()
    tool_call.id = "call_456"
    tool_call.function.name = "ping"
    tool_call.function.arguments = json.dumps({})

    captured_messages = []

    def mock_chat(messages, tools=None):
        captured_messages.append(messages.copy())
        if len(captured_messages) == 1:
            return _make_message(content=None, tool_calls=[tool_call])
        return _make_message(content="pong received")

    with patch("core.agent_loop.chat", side_effect=mock_chat):
        from core.agent_loop import run
        run("sys", "user", [], {"ping": lambda: "pong"})

    last_messages = captured_messages[-1]
    tool_results = [m for m in last_messages if m.get("role") == "tool"]
    assert len(tool_results) == 1
    assert tool_results[0]["content"] == "pong"
