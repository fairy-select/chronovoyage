from chronovoyage.internal.exception.config import TargetDirectoryNotFoundError


class InitDomainError(Exception):
    """init コマンドに関するエラー"""


class InitDomainTargetDirectoryNotFoundError(TargetDirectoryNotFoundError, InitDomainError):
    """初期化したいディレクトリの作成場所が存在しない場合に送出するエラー"""


class AddDomainError(Exception):
    """add コマンドに関するエラー"""


class AddDomainTargetDirectoryNotFoundError(TargetDirectoryNotFoundError, AddDomainError):
    """初期化したいディレクトリの作成場所が存在しない場合に送出するエラー"""


class AddDomainInvalidDescriptionError(AddDomainError):
    """period の説明が不適切な場合に送出するエラー"""

    def __init__(self) -> None:
        super().__init__("description must consist of a-z, 0-9, and underscore(_).")


class CurrentDomainError(Exception):
    """ステータス取得に関するエラー"""


class CurrentDomainDataIntegrityError(CurrentDomainError):
    """データ不整合の場合に送出するエラー"""


class CurrentDomainDbCurrentPeriodNotInMigrateConfigError(CurrentDomainDataIntegrityError):
    """DB から検出された時代が設定ファイルに見つからなかった場合に送出するエラー"""

    def __init__(self, period_name: str) -> None:
        super().__init__(f"Database says current period is '{period_name}', but not in your migrate config.")


class MigrateDomainError(Exception):
    """マイグレーションに関するエラー"""


class MigrateDomainInvalidTargetError(MigrateDomainError):
    """不適切な時代が指定された際に送出するエラー"""


class MigrateDomainUnknownTargetError(MigrateDomainInvalidTargetError):
    """存在しない時代が指定された際に送出するエラー"""

    def __init__(self) -> None:
        super().__init__("unknown target")


class MigrateDomainPastTargetError(MigrateDomainInvalidTargetError):
    """過去の時代が指定された際に送出するエラー"""

    def __init__(self) -> None:
        super().__init__("past target")


class RollbackDomainError(Exception):
    """ロールバックに関するエラー"""


class RollbackDomainSystemTableNotExistError(RollbackDomainError):
    """ロールバック時にシステムテーブルが存在しない場合に送出するエラー"""


class RollbackDomainInvalidTargetError(RollbackDomainError):
    """ロールバックで不適切な時代が指定された際に送出するエラー"""


class RollbackDomainUnknownTargetError(RollbackDomainInvalidTargetError):
    """存在しない時代が指定された際に送出するエラー"""

    def __init__(self) -> None:
        super().__init__("unknown target")


class RollbackDomainFutureTargetError(RollbackDomainInvalidTargetError):
    """ロールバックで未来の時代が指定された際に送出するエラー"""

    def __init__(self) -> None:
        super().__init__("future target")


class RollbackDomainMigratedPeriodNotInMigrateConfigError(RollbackDomainError):
    """ロールバック時にすでに到来していた時代が設定ファイルに見つからなかった場合に送出するエラー"""

    def __init__(self, period_name: str) -> None:
        super().__init__(f"Database want to rollback '{period_name}', but not in your migrate config.")
