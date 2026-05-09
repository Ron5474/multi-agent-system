from pathlib import Path
from core.agent_loop import run
from core.task_queue import get_pending, update_status
from tools.arxiv_search import arxiv_search
from tools.file_reader import read_file
from tools.memory import write_memory, append_log
from tools.discord_tools import post_to_discord

_SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "study_coach.md").read_text()

_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "arxiv_search",
            "description": "Search arXiv for a paper by title or ID to get its abstract and metadata",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a local PDF or text file",
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
            "name": "write_memory",
            "description": "Save the study note to memory",
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
            "description": "Post the study note to Discord",
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


def run_pending_tasks() -> list[str]:
    tasks = get_pending("study")
    results = []
    handlers = {
        "arxiv_search": arxiv_search,
        "read_file": read_file,
        "write_memory": write_memory,
        "append_log": append_log,
        "post_to_discord": post_to_discord,
    }
    for task in tasks:
        update_status(task["id"], "in_progress")
        result = run(_SYSTEM_PROMPT, task["payload"], _TOOLS, handlers)
        update_status(task["id"], "done")
        results.append(result)
    return results
