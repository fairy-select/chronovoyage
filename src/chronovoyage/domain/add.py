import os
import re
from datetime import datetime

from chronovoyage.internal.exception.domain import (
    AddDomainInvalidDescriptionError,
    AddDomainTargetDirectoryNotFoundError,
)
from chronovoyage.internal.logger.logger import AppLogger
from chronovoyage.internal.type.config import MigratePeriodCreateParam
from chronovoyage.internal.type.enum import MigratePeriodLanguageEnum
from chronovoyage.usecase.init import InitUsecase


class AddDomain:
    def __init__(self, cwd: str, *, logger: AppLogger) -> None:
        self._cwd = cwd
        self._logger = logger
        self.usecase = InitUsecase(logger=self._logger)

    def execute(self, language: MigratePeriodLanguageEnum, description: str, *, now: datetime) -> None:
        if not re.match(r"^[a-z0-9_]+$", description):
            raise AddDomainInvalidDescriptionError

        params = MigratePeriodCreateParam(
            period_name=now.strftime("%Y%m%d%H%M%S"),
            language=language,
            description=description,
        )
        self.usecase.create_migrate_period(self._cwd, params)

    @property
    def _cwd(self) -> str:
        return self.__cwd

    @_cwd.setter
    def _cwd(self, cwd: str) -> None:
        if not os.path.isdir(cwd):
            raise AddDomainTargetDirectoryNotFoundError(dirname=cwd)
        self.__cwd = cwd
