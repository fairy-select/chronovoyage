from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, Generator, Protocol, TypeVar

if TYPE_CHECKING:
    from chronovoyage.internal.config import MigratePeriod

T = TypeVar("T")


class PCanHandleTransaction(Protocol):
    def begin(self):
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

    @abstractmethod
    def create_if_not_exists_system_table(self) -> bool:
        """Create a table if it does not exist.

        Returns:
            bool: True if the table is created, False otherwise.

        """


class PCanUseWithClause(Protocol):
    def __enter__(self) -> Any:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class IDatabaseConnection(PCanUseWithClause, metaclass=ABCMeta):
    @abstractmethod
    def __enter__(self) -> IDatabaseConnectionWrapper:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
