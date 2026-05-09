from unittest.mock import patch, MagicMock


def _make_atom(title: str, summary: str, url: str, author: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>{title}</title>
    <summary>{summary}</summary>
    <link type="text/html" href="{url}"/>
    <author><name>{author}</name></author>
  </entry>
</feed>"""


def test_arxiv_search_returns_formatted_results():
    xml_data = _make_atom("LoRA: Low-Rank Adaptation", "LoRA fine-tunes LLMs efficiently.", "https://arxiv.org/abs/2106.09685", "Hu et al.")

    with patch("tools.arxiv_search.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = xml_data
        from tools.arxiv_search import arxiv_search
        result = arxiv_search("LoRA fine-tuning")

    assert "LoRA: Low-Rank Adaptation" in result
    assert "arxiv.org" in result
    assert "Hu et al." in result


def test_arxiv_search_returns_message_when_no_results():
    empty_feed = '<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"></feed>'

    with patch("tools.arxiv_search.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = empty_feed
        from tools.arxiv_search import arxiv_search
        result = arxiv_search("xyznonexistent")

    assert "No papers found" in result


def test_arxiv_search_handles_http_error():
    with patch("tools.arxiv_search.requests.get") as mock_get:
        mock_get.return_value.status_code = 503
        from tools.arxiv_search import arxiv_search
        result = arxiv_search("anything")

    assert "failed" in result.lower()
