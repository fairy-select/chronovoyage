from chronovoyage.internal.exception.config import TargetDirectoryNotFoundError


class InitDomainError(Exception):
    """init コマンドに関するエラー"""


class InitDomainTargetDirectoryNotFoundError(TargetDirectoryNotFoundError, InitDomainError):
    """初期化したいディレクトリの作成場所が存在しない場合に送出するエラー"""
