from pathlib import Path
from datetime import datetime

MEMORY_DIR = Path("memory")


def read_memory(filename: str) -> str:
    path = MEMORY_DIR / filename
    if not path.exists():
        return ""
    return path.read_text()


def write_memory(filename: str, content: str) -> str:
    path = MEMORY_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return f"Written to {filename}"


def append_log(entry: str) -> str:
    path = MEMORY_DIR / "daily_log.md"
    path.parent.mkdir(exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open(path, "a") as f:
        f.write(f"\n## {timestamp}\n{entry}\n")
    return "Logged"
