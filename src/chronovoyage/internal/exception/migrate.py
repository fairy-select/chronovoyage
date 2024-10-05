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


class RollbackError(Exception):
    """ロールバックに関するエラー"""


class RollbackSystemTableNotExistError(RollbackError):
    """ロールバック時にシステムテーブルが存在しない場合に送出するエラー"""


class RollbackInvalidTargetError(RollbackError):
    """ロールバックで不適切な時代が指定された際に送出するエラー"""


class RollbackUnknownTargetError(RollbackInvalidTargetError):
    """存在しない時代が指定された際に送出するエラー"""

    def __init__(self) -> None:
        super().__init__("unknown target")


class RollbackFutureTargetError(RollbackInvalidTargetError):
    """ロールバックで未来の時代が指定された際に送出するエラー"""

    def __init__(self) -> None:
        super().__init__("future target")


class RollbackMigratedPeriodNotInMigrateConfigError(RollbackError):
    """ロールバック時にすでに到来していた時代が設定ファイルに見つからなかった場合に送出するエラー"""

    def __init__(self, period_name: str) -> None:
        super().__init__(f"Database want to rollback '{period_name}', but not in your migrate config.")
