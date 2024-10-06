from enum import Enum

from chronovoyage.internal.exception.enum import InvalidDatabaseVendorValueError


class StrEnum(Enum):
    def __eq__(self, __value):
        if isinstance(__value, self.__class__):
            return self.value == __value.value
        if isinstance(__value, str):
            return self.value == __value
        return super().__eq__(__value)

    def __hash__(self):
        return super().__hash__()


class DatabaseVendorEnum(StrEnum):
    MARIADB = "mariadb"
    MYSQL = "mysql"

    @classmethod
    def _missing_(cls, _):
        raise InvalidDatabaseVendorValueError


class MigratePeriodLanguageEnum(StrEnum):
    DDL = "ddl"
    DML = "dml"


class FeatureFlagEnum(StrEnum):
    ROLLBACK_WITHOUT_OPTIONS = "rollback_without_options"
