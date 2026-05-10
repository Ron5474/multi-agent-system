from datetime import datetime
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/Los_Angeles")


def local_now() -> datetime:
    return datetime.now(LOCAL_TZ)


def local_now_str(fmt: str = "%Y-%m-%d %H:%M %Z") -> str:
    return local_now().strftime(fmt)
