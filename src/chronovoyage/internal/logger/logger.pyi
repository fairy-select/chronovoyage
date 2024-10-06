class BaseAppLogger:
    def debug(self, msg: object, *args: object) -> None: ...
    def info(self, msg: object, *args: object) -> None: ...
    def warning(self, msg: object, *args: object) -> None: ...
    def error(self, msg: object, *args: object) -> None: ...
    def exception(self, msg: object, *args: object, **kwargs) -> None: ...

class AppLogger(BaseAppLogger): ...
class AppLoggerDebug(BaseAppLogger): ...

class AppLoggerFactory:
    __verbose: bool

    @classmethod
    def set_verbose(cls, *, verbose: bool) -> None: ...
    @classmethod
    def get_instance(cls) -> AppLoggerDebug | AppLogger: ...

def get_default_logger() -> AppLogger: ...
