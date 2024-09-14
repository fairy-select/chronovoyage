import string
from datetime import datetime
from logging import Logger

from chronovoyage.internal.config import MigrateDomainConfig
from chronovoyage.internal.type.enum import MigratePeriodLanguageEnum
from chronovoyage.usecase.init import InitUsecase


class AddDomain:
    def __init__(self, config: MigrateDomainConfig, *, logger: Logger) -> None:
        self._config = config
        self._logger = logger
        self.usecase = InitUsecase(logger=self._logger)

    def execute(self, language: MigratePeriodLanguageEnum, description: str, *, now: datetime) -> None:
        directory_name = string.Template("${date}_${language}_${description}").safe_substitute(date=now.strftime("%Y%m%d%H%M%S"), language=language, description=description)
        self.usecase.create_migrate_period(directory_name)
