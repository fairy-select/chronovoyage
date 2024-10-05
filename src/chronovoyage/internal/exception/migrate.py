class MigrateError(Exception):
    """マイグレーションに関するエラー"""


class MigrateInvalidTargetError(MigrateError):
    """不適切な時代が指定された際に送出するエラー"""


class MigrateUnknownTargetError(MigrateInvalidTargetError):
    """存在しない時代が指定された際に送出するエラー"""

    def __init__(self) -> None:
        super().__init__("unknown target")


class MigratePastTargetError(MigrateInvalidTargetError):
    """過去の時代が指定された際に送出するエラー"""

    def __init__(self) -> None:
        super().__init__("past target")


class RollbackInvalidTargetError(MigrateError):
    """ロールバックで不適切な時代が指定された際に送出するエラー"""


class RollbackFutureTargetError(RollbackInvalidTargetError):
    """ロールバックで未来の時代が指定された際に送出するエラー"""

    def __init__(self) -> None:
        super().__init__("future target")
