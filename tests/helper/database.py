from helper import DEFAULT_TEST_ENV

from chronovoyage.database.connection import ConnectionInfo, DatabaseConnector, DatabaseVendor


class DatabaseHelper:
    # noinspection PyMethodMayBeStatic
    def get_connection(self, vendor: DatabaseVendor):
        database_connector = DatabaseConnector()
        if vendor == "mariadb":
            connection_info = ConnectionInfo(
                user=DEFAULT_TEST_ENV["MARIADB_USER"],
                password=DEFAULT_TEST_ENV["MARIADB_PASSWORD"],
                host="127.0.0.1",
                port=3307,
            )
            return database_connector.get_connection("mariadb", connection_info)

        return None
