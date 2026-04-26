import os
from pathlib import Path
from dotenv import load_dotenv
from core.agent_loop import run
from core.task_queue import add_task
from tools.memory import write_memory, append_log
from tools.file_reader import read_file, list_files
from tools.discord_tools import post_to_discord

load_dotenv()

_SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "assignment_scout.md").read_text()
_SCHOOL_DIR = os.getenv("SCHOOL_FILES_DIR", ".")

_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in the school files directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string"},
                    "extension": {"type": "string", "description": "Optional file extension filter (e.g. 'pdf')"},
                },
                "required": ["directory"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file (text or PDF)",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a task to the queue",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "description": "Task type: school, research"},
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


def run_scan() -> str:
    handlers = {
        "list_files": list_files,
        "read_file": read_file,
        "add_task": add_task,
        "write_memory": write_memory,
        "append_log": append_log,
        "post_to_discord": post_to_discord,
    }
    return run(
        _SYSTEM_PROMPT,
        f"Scan the school files directory at {_SCHOOL_DIR} for upcoming deadlines.",
        _TOOLS,
        handlers,
    )
