import requests
import xml.etree.ElementTree as ET

_BASE_URL = "https://export.arxiv.org/api/query"
_NS = {"atom": "http://www.w3.org/2005/Atom"}


def arxiv_search(query: str, max_results: int = 5) -> str:
    params = {
        "search_query": f"all:{query}",
        "max_results": max_results,
        "sortBy": "relevance",
    }
    resp = requests.get(_BASE_URL, params=params, timeout=15)
    if resp.status_code != 200:
        return f"arXiv request failed: HTTP {resp.status_code}"

    root = ET.fromstring(resp.text)
    entries = root.findall("atom:entry", _NS)
    if not entries:
        return "No papers found."

    results = []
    for entry in entries:
        title = entry.findtext("atom:title", "", _NS).strip().replace("\n", " ")
        summary = entry.findtext("atom:summary", "", _NS).strip().replace("\n", " ")[:300]
        url = next(
            (l.get("href") for l in entry.findall("atom:link", _NS) if l.get("type") == "text/html"),
            entry.findtext("atom:id", "", _NS),
        )
        authors = [a.findtext("atom:name", "", _NS) for a in entry.findall("atom:author", _NS)]
        author_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
        results.append(f"**{title}**\n{author_str}\n{url}\n{summary}...")

    return "\n\n".join(results)
