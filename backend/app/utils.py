from datetime import datetime, timedelta, timezone
from typing import Literal


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def get_device_status(
    *, last_seen: datetime | None, created_at: datetime
) -> Literal["online", "offline", "initialized"]:
    now = utc_now()

    if last_seen is None:
        if now - created_at < timedelta(hours=2):
            return "initialized"
        return "offline"
    return "online" if last_seen > now - timedelta(minutes=120) else "offline"
