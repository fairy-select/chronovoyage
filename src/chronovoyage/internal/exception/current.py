class CurrentError(Exception):
    """ステータス取得に関するエラー"""


class CurrentDataIntegrityError(CurrentError):
    """データ不整合の場合に送出するエラー"""


class CurrentDbCurrentPeriodNotInMigrateConfigError(CurrentDataIntegrityError):
    """DB から検出された時代が設定ファイルに見つからなかった場合に送出するエラー"""

    def __init__(self, period_name: str) -> None:
        super().__init__(f"Database says current period is '{period_name}', but not in your migrate config.")
