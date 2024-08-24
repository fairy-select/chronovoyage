class TestConnection:
    def test_connect_to_mariadb(self, database_helper) -> None:
        cnx = database_helper.get_connection('mariadb')
        assert cnx is not None
