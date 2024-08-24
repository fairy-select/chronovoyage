from logging import Logger


class マイグレーション実行クラス:
    def __init__(self, *, 接続設定, logger: Logger) -> None:
        self._logger = logger
        self._データベースに接続する()

    def _データベースに接続する(self):
        self._logger.info("データベースに接続")

    def マイグレーションを実行する(self):
        self._logger.info("マイグレーションを実行する")
