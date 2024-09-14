from datetime import datetime
from logging import Logger

from chronovoyage.internal.type.config import MigratePeriodCreateParam
from chronovoyage.internal.type.enum import MigratePeriodLanguageEnum
from chronovoyage.usecase.init import InitUsecase


class AddDomain:
    def __init__(self, *, logger: Logger) -> None:
        self._logger = logger
        self.usecase = InitUsecase(logger=self._logger)

    def execute(self, language: MigratePeriodLanguageEnum, description: str, *, now: datetime, to_directory: str) -> None:
        params = MigratePeriodCreateParam(
            period_name=now.strftime("%Y%m%d%H%M%S"),
            language=language,
            description=description,
        )
        self.usecase.create_migrate_period(to_directory, params)
