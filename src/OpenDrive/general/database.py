"""
@author: Julian Sobott
@brief: Tools for accessing a sqlite database
@description:

@external_use:

@internal_use:
"""
import sqlite3


class DBConnection:
    """Interface to a sqlite database. Used as context-manager, to properly open and close the connection"""

    def __init__(self, abs_db_path: str) -> None:
        self.abs_db_path = abs_db_path
        self.connection: sqlite3.Connection
        self.cursor: sqlite3.Cursor

    def __enter__(self) -> 'DBConnection':
        """Opens a connection in initializes the cursor"""
        self.connection = sqlite3.connect(self.abs_db_path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the connection"""
        self.connection.commit()
        self.connection.close()

    def get(self, sql: str, args: tuple = ()) -> list:
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    def create(self, sql: str, args: tuple = ()) -> None:
        self.cursor.execute(sql, args)

    def insert(self, sql: str, args: tuple = ()) -> int:
        self.cursor.execute(sql, args)
        return self.cursor.lastrowid

    def update(self, sql: str, args: tuple = ()) -> None:
        self.cursor.execute(sql, args)

    def delete(self, sql: str, args: tuple = ()) -> None:
        self.cursor.execute(sql, args)


class TableEntry(object):

    def __init__(self, db_path: str, table_name: str, primary_id_name: str):
        self._id = -1
        self._db_path = db_path
        self._table_name = table_name
        self._primary_id_name = primary_id_name

    @property
    def id(self):
        return self._id

    def update(self):
        self.__init__(self.id)
        return self

    def _change_field(self, field_name: str, new_value) -> None:
        if ";" in field_name or ")" in field_name:
            raise ValueError("Preventing possible sql injection")
        sql = f'UPDATE "{self._table_name}" SET {field_name} = ? WHERE "{self._primary_id_name}" = ?'
        with DBConnection(self._db_path) as db:
            db.update(sql, (new_value, self.id))
