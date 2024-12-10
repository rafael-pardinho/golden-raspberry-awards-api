import sqlite3

class SQLiteHandler:
    def __init__(self, database_path=":memory:"):
        self.connection = sqlite3.connect(database_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row

    def get_connection(self):
        return self.connection