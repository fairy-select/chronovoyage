class DatabaseError(Exception):
    """データベースに関するエラー"""
    pass

class DatabaseUnknownVendorError(DatabaseError):
    """想定外のデータベースベンダーが与えられたときに創出するエラー"""
    pass
