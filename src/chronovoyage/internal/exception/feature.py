from chronovoyage.internal.type.enum import FeatureFlagEnum


class FeatureNotSupportedError(Exception):
    """まだ開発中でリリースされていない機能にアクセスされた場合に送出するエラー"""

    def __init__(self, feature: FeatureFlagEnum) -> None:
        s = feature.value.capitalize().replace("_", " ")
        super().__init__(f"'{s}' is currently not supported")


class FeatureFlagNotDefinedError(Exception):
    """定義されていないフィーチャーフラグが参照された場合に送出するエラー"""

    def __init__(self, feature: FeatureFlagEnum) -> None:
        s = feature.value.capitalize().replace("_", " ")
        super().__init__(f"'{s}' is not defined")
