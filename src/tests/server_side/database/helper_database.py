from OpenDrive.server_side import database, paths
from OpenDrive.general.database import delete_db_file


def h_setup_server_database():
    """clear and create the server database file."""
    delete_db_file(paths.SERVER_DB_PATH)
    database.create_database()
