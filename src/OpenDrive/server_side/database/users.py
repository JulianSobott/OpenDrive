"""
:module: OpenDrive.server_side.database.users
:synopsis: DB class for the users table
:author: Julian Sobott

public classes
---------------

.. autoclass:: User
    :exclude-members: DB_PATH
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:

"""
from typing import Optional

from OpenDrive.general.database import TableEntry, DBConnection
from OpenDrive.server_side import paths


class User(TableEntry):
    """
    :ivar user_id:
    :ivar username:
    :ivar password:
    :ivar email:
    """

    TABLE_NAME = "users"
    DB_PATH = paths.SERVER_DB_PATH
    PRIMARY_KEY_NAME = "user_id"

    def __init__(self,
                 user_id: int,
                 username: str,
                 password: str,
                 email: Optional[str] = None) -> None:
        super().__init__()
        self._id = user_id
        self._username = username
        self._password = password
        self._email = email

    @staticmethod
    def create(username: str,
               password: str,
               email: Optional[str] = None) -> int:
        sql = "INSERT INTO `users` (username, password, email) VALUES (?, ?, ?)"
        with DBConnection(paths.SERVER_DB_PATH) as db:
            user_id = db.insert(sql, (username, password, email))
            return user_id

    """user_id"""

    @property
    def user_id(self) -> int:
        return self._id

    """username"""

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, val: str) -> None:
        self._change_field("username", val)

    """password"""

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, val: str) -> None:
        self._change_field("password", val)

    """email"""

    @property
    def email(self) -> Optional[str]:
        return self._email

    @email.setter
    def email(self, val: Optional[str]) -> None:
        self._change_field("email", val)

    """Get by`s"""

    @classmethod
    def get_by_username(cls, username) -> Optional['User']:
        entries = cls.from_columns("username = ?", (username,))
        assert len(entries) <= 1, "Non unique username in table 'users'!"
        if len(entries) == 0:
            return None
        user: User = entries[0]
        return user

    def __repr__(self):
        return f"User({self._id}, {self._username}, {self._password}, {self._email})"
