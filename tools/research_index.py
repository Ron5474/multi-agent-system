from pathlib import Path

_RESEARCH_DIR = Path("memory/research")


def find_related_research(topic: str) -> str:
    """Search saved research files for content related to topic. Returns matches or empty string."""
    if not _RESEARCH_DIR.exists():
        return ""

    keywords = set(w.lower() for w in topic.replace("-", " ").split() if len(w) > 3)
    matches = []

    for path in sorted(_RESEARCH_DIR.glob("*.md")):
        content = path.read_text().lower()
        hits = sum(1 for kw in keywords if kw in content)
        if hits >= 2:
            # grab the first non-empty line as a title
            title = next((l.strip("# \n") for l in path.read_text().splitlines() if l.strip()), path.stem)
            matches.append((hits, title, path.name))

    if not matches:
        return ""

    matches.sort(reverse=True)
    lines = [f"- [{title}](memory/research/{fname})" for _, title, fname in matches]
    return "Related research you've done:\n" + "\n".join(lines)
