from logging import Logger


class InitUsecase:
    def __init__(self, *, logger: Logger) -> None:
        self._logger = logger

    def create_files(self, *, to_directory: str) -> None:
        pass
