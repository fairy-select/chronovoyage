class InitDomainError(Exception):
    """init コマンドに関するエラー"""


class InitDomainTargetDirectoryNotFoundError(InitDomainError):
    """初期化したいディレクトリの作成場所が存在しない場合に送出するエラー"""

    def __init__(self, *, dirname: str) -> None:
        super().__init__(f"{dirname} is not a directory")
