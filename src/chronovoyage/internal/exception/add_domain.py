from chronovoyage.internal.exception.config import TargetDirectoryNotFoundError


class AddDomainError(Exception):
    """add コマンドに関するエラー"""


class AddDomainTargetDirectoryNotFoundError(TargetDirectoryNotFoundError, AddDomainError):
    """初期化したいディレクトリの作成場所が存在しない場合に送出するエラー"""


class AddDomainInvalidDescriptionError(AddDomainError):
    """period の説明が不適切な場合に送出するエラー"""

    def __init__(self) -> None:
        super().__init__("description must consist of a-z, 0-9, and underscore(_).")
