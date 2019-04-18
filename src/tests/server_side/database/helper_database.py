from OpenDrive.server_side import database, paths
from OpenDrive.general.database import delete_db_file


def h_setup_server_database() -> None:
    """clear and create the server database file."""
    delete_db_file(paths.SERVER_DB_PATH)
    database.create_database()


def h_create_dummy_user() -> database.User:
    username = "Tom"
    password = "asj&kdkl$asjd345a!d:-"
    email = "Tom@gmail.com"
    user_id = database.User.create(username, password, email)
    return database.User(user_id, username, password, email)
