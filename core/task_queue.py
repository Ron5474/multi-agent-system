import json
import uuid
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path("memory/tasks.json")


def _load() -> list[dict]:
    if not TASKS_FILE.exists():
        return []
    return json.loads(TASKS_FILE.read_text())


def _save(tasks: list[dict]) -> None:
    TASKS_FILE.parent.mkdir(exist_ok=True)
    TASKS_FILE.write_text(json.dumps(tasks, indent=2))


def add_task(type: str, payload: str) -> dict:
    tasks = _load()
    task = {
        "id": str(uuid.uuid4()),
        "type": type,
        "payload": payload,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
    }
    tasks.append(task)
    _save(tasks)
    return task


def get_pending(type: str) -> list[dict]:
    return [t for t in _load() if t["type"] == type and t["status"] == "pending"]


def update_status(task_id: str, status: str) -> None:
    tasks = _load()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
    _save(tasks)


def list_tasks(type: str | None = None) -> list[dict]:
    tasks = _load()
    if type:
        return [t for t in tasks if t["type"] == type]
    return tasks
