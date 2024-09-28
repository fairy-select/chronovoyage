class InvalidDatabaseVendorValueError(ValueError):
    def __init__(self):
        super().__init__("Given database vendor is invalid")
