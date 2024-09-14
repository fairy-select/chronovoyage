class MigrateError(Exception):
    """マイグレーションに関するエラー"""
    pass


class MigrateInvalidTargetError(MigrateError):
    """不適切な時代が指定された際に送出するエラー"""
    pass
