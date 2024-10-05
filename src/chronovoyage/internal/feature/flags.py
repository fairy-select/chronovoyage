from typing import Callable, ClassVar, Mapping

from chronovoyage.internal.exception.feature import FeatureFlagNotDefinedError, FeatureNotSupportedError
from chronovoyage.internal.type.enum import FeatureFlagEnum

flags: Mapping[FeatureFlagEnum, bool] = {FeatureFlagEnum.ROLLBACK_WITHOUT_OPTIONS: False}


class FeatureFlagEnabledMeta(type):
    __flags: ClassVar[Mapping[FeatureFlagEnum, bool]] = flags

    def __getattr__(cls, attr) -> bool:
        flag_enum = FeatureFlagEnum(attr)
        flag = cls.__flags.get(flag_enum)
        if flag is None:
            raise FeatureFlagNotDefinedError(flag_enum)
        return flag


class FeatureFlagEnabled(metaclass=FeatureFlagEnabledMeta):
    """Get feature flag.

    True if enabled, False otherwise for each flag.

    """

    def __getattr__(self, attr):
        return getattr(type(self), attr)


class FeatureFlagEnabledCheckerMeta(type):
    __flags: ClassVar[Mapping[FeatureFlagEnum, bool]] = flags

    def __getattr__(cls, attr) -> Callable[[], None]:
        def wrapper() -> None:
            flag_enum = FeatureFlagEnum(attr)
            flag = cls.__flags.get(flag_enum)
            if flag is None:
                raise FeatureFlagNotDefinedError(flag_enum)
            if not flag:
                raise FeatureNotSupportedError(flag_enum)

        return wrapper


class FeatureFlagEnabledChecker(metaclass=FeatureFlagEnabledCheckerMeta):
    """Check feature flag enabled.

    It returns exception if feature flag is not enabled.

    """

    def __getattr__(self, attr):
        return getattr(type(self), attr)
