class FeatureFlagEnabled:
    @property
    def rollback_without_options(self) -> bool: ...

class FeatureFlagEnabledChecker:
    @classmethod
    def rollback_without_options(cls) -> None: ...
