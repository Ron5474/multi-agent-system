# tests/test_discord_tools.py
from unittest.mock import patch


def test_post_to_discord_sends_request():
    with patch("tools.discord_tools._WEBHOOKS", {"system": "https://discord.com/api/webhooks/test"}):
        with patch("tools.discord_tools.requests.post") as mock_post:
            mock_post.return_value.status_code = 204
            from tools.discord_tools import post_to_discord
            result = post_to_discord("system", "health check passed")
    mock_post.assert_called_once()
    assert "Posted" in result


def test_post_to_discord_unknown_channel_returns_error():
    from tools.discord_tools import post_to_discord
    result = post_to_discord("unknown-channel", "hello")
    assert "No webhook" in result
