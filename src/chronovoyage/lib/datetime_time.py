from __future__ import annotations

from datetime import datetime, timezone


class DatetimeLib:
    DEFAULT_TIMEZONE = timezone.utc

    @classmethod
    def now(cls) -> datetime:
        return datetime.now(tz=cls.DEFAULT_TIMEZONE)

    @classmethod
    def datetime(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tzinfo: timezone | None = None,
    ) -> datetime:
        return datetime(year, month, day, hour, minute, second, microsecond, tzinfo=tzinfo or cls.DEFAULT_TIMEZONE)
