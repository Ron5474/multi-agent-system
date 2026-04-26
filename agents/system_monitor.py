import shutil
import psutil
from pathlib import Path
from core.agent_loop import run
from tools.memory import read_memory, append_log
from tools.discord_tools import post_to_discord

_SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "system_monitor.md").read_text()

_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_disk",
            "description": "Check disk usage on the root filesystem",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_processes",
            "description": "Get a summary of running processes",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_memory",
            "description": "Read a memory file by filename",
            "parameters": {
                "type": "object",
                "properties": {"filename": {"type": "string", "description": "Relative path within memory/"}},
                "required": ["filename"],
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
                    "channel": {"type": "string", "description": "Channel name: system, school, research, general, morning-brief, tasks"},
                    "message": {"type": "string"},
                },
                "required": ["channel", "message"],
            },
        },
    },
]


def _check_disk() -> str:
    usage = shutil.disk_usage("/")
    pct = usage.used / usage.total * 100
    return f"Total: {usage.total / 1e9:.1f}GB, Used: {usage.used / 1e9:.1f}GB ({pct:.0f}%), Free: {usage.free / 1e9:.1f}GB"


def _check_processes() -> str:
    procs = list(psutil.process_iter(["pid", "name", "status"]))
    running = [p for p in procs if p.info["status"] == psutil.STATUS_RUNNING]
    return f"{len(procs)} total processes, {len(running)} actively running"


def run_health_check() -> str:
    handlers = {
        "check_disk": _check_disk,
        "check_processes": _check_processes,
        "read_memory": read_memory,
        "append_log": append_log,
        "post_to_discord": post_to_discord,
    }
    return run(_SYSTEM_PROMPT, "Run the health check now.", _TOOLS, handlers)
