from enum import Enum


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


class MigratePeriodLanguageEnum(StrEnum):
    DDL = "ddl"
    DML = "dml"
