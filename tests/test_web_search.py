# tests/test_web_search.py
from unittest.mock import patch, MagicMock


def test_web_search_returns_formatted_results():
    mock_results = [
        {"title": "Result 1", "href": "https://example.com", "body": "Some text"},
        {"title": "Result 2", "href": "https://other.com", "body": "More text"},
    ]
    with patch("tools.web_search.DDGS") as MockDDGS:
        instance = MockDDGS.return_value.__enter__.return_value
        instance.text.return_value = mock_results
        from tools.web_search import web_search
        result = web_search("test query")
    assert "Result 1" in result
    assert "https://example.com" in result
    assert "Some text" in result


def test_web_search_returns_message_when_no_results():
    with patch("tools.web_search.DDGS") as MockDDGS:
        instance = MockDDGS.return_value.__enter__.return_value
        instance.text.return_value = []
        from tools.web_search import web_search
        result = web_search("obscure query")
    assert "No results" in result
