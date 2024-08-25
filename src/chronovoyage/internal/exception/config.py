class MigrateConfigError(Exception):
    """マイグレーション設定がルールに沿っていない場合に送出するエラー"""


class MigrateConfigVersionNameInvalidError(MigrateConfigError):
    """マイグレーションの各バージョンのディレクトリが命名規則に合っていない場合に送出するエラー"""


class MigrateConfigSqlMissingError(MigrateConfigError):
    """go.sql または return.sql が存在しない場合に送出するエラー"""


class MigrateConfigGoSqlMissingError(MigrateConfigSqlMissingError):
    """go.sql が存在しない場合に送出するエラー"""


class MigrateConfigReturnSqlMissingError(MigrateConfigSqlMissingError):
    """return.sql が存在しない場合に送出するエラー"""
