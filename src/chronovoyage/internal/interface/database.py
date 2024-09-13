from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, Generator, Protocol, TypeVar

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigratePeriod

T = TypeVar("T")


class PCanHandleTransaction(Protocol):
    def _begin(self):
        pass


class IDatabaseConnectionWrapper(PCanHandleTransaction, metaclass=ABCMeta):
    @abstractmethod
    def add_period(self, period: MigratePeriod) -> int:
        pass

    @abstractmethod
    def get_sqls(self, filepath: str) -> Generator[str, Any, None]:
        pass

    @abstractmethod
    def execute_sql(self, sql: str) -> None:
        pass

    @abstractmethod
    def mark_period_as_come(self, inserted_period_id: int) -> None:
        pass

    @abstractmethod
    def get_current_period(self) -> str | None:
        pass


class PCanUseWithClause(Protocol):
    def __enter__(self) -> Any:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class IDatabaseConnection(PCanUseWithClause, metaclass=ABCMeta):
    def __enter__(self) -> IDatabaseConnectionWrapper:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
