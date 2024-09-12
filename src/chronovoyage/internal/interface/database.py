from typing import Protocol, TypeVar

T = TypeVar("T")


class PCanHandleTransaction(Protocol):
    def begin(self):
        pass


class PCanUseWithClause(Protocol):
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class IDatabaseConnection(PCanUseWithClause):
    pass
