from chronovoyage.internal.exception.config import TargetDirectoryNotFoundError


class AddDomainError(Exception):
    """add コマンドに関するエラー"""
    pass


class AddDomainTargetDirectoryNotFoundError(TargetDirectoryNotFoundError, AddDomainError):
    """初期化したいディレクトリの作成場所が存在しない場合に送出するエラー"""
    pass
