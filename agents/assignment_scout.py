from pathlib import Path
from core.agent_loop import run
from core.task_queue import add_task
from tools.memory import write_memory, append_log
from tools.canvas import get_upcoming_assignments
from tools.custom_deadlines import get_upcoming_custom
from tools.research_index import find_related_research
from tools.discord_tools import post_to_discord

_SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "assignment_scout.md").read_text()

_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_upcoming_assignments",
            "description": "Fetch upcoming assignments from Canvas LMS within a given number of days",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "description": "How many days ahead to look (default 14)"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_upcoming_custom",
            "description": "Fetch manually added deadlines (exams, etc.) within a given number of days",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "description": "How many days ahead to look (default 14)"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_related_research",
            "description": "Search saved research summaries for content related to an assignment or topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Assignment name or topic to search for"},
                },
                "required": ["topic"],
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
                    "type": {"type": "string", "description": "Task type: school or research"},
                    "payload": {"type": "string"},
                },
                "required": ["type", "payload"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_memory",
            "description": "Save scan results to memory",
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
            "name": "post_to_discord",
            "description": "Post a message to a Discord channel. Provide title to send as a rich embed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "channel": {"type": "string"},
                    "message": {"type": "string"},
                    "title": {"type": "string", "description": "Optional embed title for structured outputs."},
                },
                "required": ["channel", "message"],
            },
        },
    },
]


def run_scan() -> str:
    handlers = {
        "get_upcoming_assignments": get_upcoming_assignments,
        "get_upcoming_custom": get_upcoming_custom,
        "find_related_research": find_related_research,
        "add_task": add_task,
        "write_memory": write_memory,
        "append_log": append_log,
        "post_to_discord": post_to_discord,
    }
    return run(
        _SYSTEM_PROMPT,
        "Fetch upcoming assignments from Canvas and any manually added deadlines. "
        "For each assignment, call find_related_research with the assignment name to check if Ron has relevant research saved. "
        "Include any matches in the report.",
        _TOOLS,
        handlers,
    )
