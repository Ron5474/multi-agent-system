from datetime import datetime
from pathlib import Path
from core.agent_loop import run
from core.task_queue import add_task, list_tasks, remove_task
from tools.memory import read_memory, write_memory, append_log, check_stale_memory
from tools.discord_tools import post_to_discord
from tools.custom_deadlines import add_deadline, remove_deadline, list_deadlines

_SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "chief_of_staff.md").read_text()

_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_memory",
            "description": "Read a memory file",
            "parameters": {
                "type": "object",
                "properties": {"filename": {"type": "string"}},
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_memory",
            "description": "Write content to a memory file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "append_log",
            "description": "Append an entry to the daily log",
            "parameters": {
                "type": "object",
                "properties": {"entry": {"type": "string"}},
                "required": ["entry"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a task to the agent queue",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "description": "Task type: research or school"},
                    "payload": {"type": "string"},
                },
                "required": ["type", "payload"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List tasks in the queue",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "description": "Optional filter by type"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_task",
            "description": "Remove a task from the queue by its id",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_stale_memory",
            "description": "Check which memory files have not been updated in a given number of days",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "description": "Staleness threshold in days (default 90)"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_deadline",
            "description": "Save a custom deadline (exam, assignment not on Canvas, etc.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the deadline"},
                    "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format"},
                    "course": {"type": "string", "description": "Course name or code (optional)"},
                },
                "required": ["name", "due_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_deadline",
            "description": "Remove a custom deadline by its id",
            "parameters": {
                "type": "object",
                "properties": {
                    "deadline_id": {"type": "string"},
                },
                "required": ["deadline_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_deadlines",
            "description": "List all saved custom deadlines",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "post_to_discord",
            "description": "Post a message to a Discord channel",
            "parameters": {
                "type": "object",
                "properties": {
                    "channel": {"type": "string"},
                    "message": {"type": "string"},
                },
                "required": ["channel", "message"],
            },
        },
    },
]

_HANDLERS = {
    "read_memory": read_memory,
    "write_memory": write_memory,
    "append_log": append_log,
    "check_stale_memory": check_stale_memory,
    "add_task": add_task,
    "list_tasks": list_tasks,
    "remove_task": remove_task,
    "add_deadline": add_deadline,
    "remove_deadline": remove_deadline,
    "list_deadlines": list_deadlines,
    "post_to_discord": post_to_discord,
}


def handle_message(user_message: str) -> str:
    return run(_SYSTEM_PROMPT, user_message, _TOOLS, _HANDLERS)


def send_morning_brief() -> str:
    today = datetime.now().strftime("%A, %B %-d, %Y")
    return run(_SYSTEM_PROMPT, f"Send the morning brief now. Today's date is {today}.", _TOOLS, _HANDLERS)


def consolidate_memory() -> str:
    today = datetime.now().strftime("%A, %B %-d, %Y")
    return run(_SYSTEM_PROMPT, f"Run nightly memory consolidation now. Today is {today}.", _TOOLS, _HANDLERS)


def weekly_reflection() -> str:
    now = datetime.now()
    week_label = f"{now.year}-W{now.isocalendar()[1]:02d}"
    return run(_SYSTEM_PROMPT, f"Generate the weekly reflection now. Week: {week_label}.", _TOOLS, _HANDLERS)
