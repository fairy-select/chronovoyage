from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class ISupportDb(Generic[T], metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_default_connection():
        pass

    @staticmethod
    @abstractmethod
    def _get_tables(cursor: T) -> set[str]:
        pass

    @staticmethod
    @abstractmethod
    def _get_system_tables(cursor: T) -> set[str]:
        pass

    @classmethod
    @abstractmethod
    def get_tables(cls) -> set[str]:
        pass

    @classmethod
    @abstractmethod
    def all_periods_have_come(cls) -> bool:
        pass

    @classmethod
    @abstractmethod
    def assert_rows_and_sql(cls, want_rows: list[tuple[Any, ...]], sql: str) -> None:
        pass

    @classmethod
    @abstractmethod
    def truncate_test_db(cls) -> None:
        pass
