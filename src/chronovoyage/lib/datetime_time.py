from datetime import datetime


class DatetimeLib:
    @classmethod
    def now(cls) -> datetime:
        return datetime.now()
