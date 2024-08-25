class DatabaseError(Exception):
    """データベースに関するエラー"""


class DatabaseUnknownVendorError(DatabaseError):
    """想定外のデータベースベンダーが与えられたときに送出するエラー"""
