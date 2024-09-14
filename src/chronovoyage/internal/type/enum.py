from enum import Enum


class DatabaseVendorEnum(str, Enum):
    MARIADB = "mariadb"


class MigratePeriodLanguageEnum(str, Enum):
    DDL = "ddl"
    DML = "dml"
