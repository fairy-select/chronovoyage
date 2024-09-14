import os.path
from logging import Logger

from chronovoyage.internal.exception.init import InitDomainTargetDirectoryNotFoundError
from chronovoyage.usecase.init import InitUsecase


class InitDomain:
    def __init__(self, cwd: str, *, logger: Logger) -> None:
        self._cwd = cwd
        self._logger = logger
        self.usecase = InitUsecase(logger=self._logger)

    def execute(self, dirname: str) -> None:
        self.usecase.create_files(to_directory=os.path.join(self._cwd, dirname))

    @property
    def _cwd(self) -> str:
        return self.__cwd

    @_cwd.setter
    def _cwd(self, cwd: str) -> None:
        if not os.path.isdir(cwd):
            raise InitDomainTargetDirectoryNotFoundError(dirname=cwd)
        self.__cwd = cwd
