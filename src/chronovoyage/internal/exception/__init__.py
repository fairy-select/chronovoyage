class DirectoryAlreadyExistsError(Exception):
    """ディレクトリが既に存在する場合に送出するエラー"""

    def __init__(self, directory: str) -> None:
        super().__init__(f"{directory} already exists")
