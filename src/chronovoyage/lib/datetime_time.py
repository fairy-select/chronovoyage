from datetime import datetime, timezone


class DatetimeLib:
    DEFAULT_TIMEZONE = timezone.utc

    @classmethod
    def now(cls) -> datetime:
        return datetime.now(tz=cls.DEFAULT_TIMEZONE)

    @classmethod
    def datetime(cls, *args) -> datetime:
        return datetime(*args, tzinfo=cls.DEFAULT_TIMEZONE)
