import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

MEMORY_DIR = Path("memory")
_METADATA_FILE = MEMORY_DIR / "_metadata.json"


def _load_metadata() -> dict:
    if not _METADATA_FILE.exists():
        return {}
    return json.loads(_METADATA_FILE.read_text())


def _stamp(filename: str) -> None:
    metadata = _load_metadata()
    metadata[filename] = datetime.now(timezone.utc).isoformat()
    _METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    _METADATA_FILE.write_text(json.dumps(metadata, indent=2))


def read_memory(filename: str) -> str:
    path = MEMORY_DIR / filename
    if not path.exists():
        return ""
    return path.read_text()


def write_memory(filename: str, content: str) -> str:
    path = MEMORY_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    _stamp(filename)
    return f"Written to {filename}"


def check_stale_memory(days: int = 90) -> str:
    metadata = _load_metadata()
    if not metadata:
        return "No memory files have been written yet."
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    stale = []
    for filename, ts in metadata.items():
        last_updated = datetime.fromisoformat(ts)
        if last_updated < cutoff:
            age = (datetime.now(timezone.utc) - last_updated).days
            stale.append(f"- {filename} (last updated {age} days ago)")
    if not stale:
        return f"All memory files updated within the last {days} days."
    return f"Stale memory files (not updated in {days}+ days):\n" + "\n".join(stale)


def append_log(entry: str) -> str:
    path = MEMORY_DIR / "daily_log.md"
    path.parent.mkdir(exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open(path, "a") as f:
        f.write(f"\n## {timestamp}\n{entry}\n")
    return "Logged"
