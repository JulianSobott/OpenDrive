import client_side
from general.database import delete_db_file


def h_delete_recreate_client_db():
    delete_db_file(client_side.paths.LOCAL_DB_PATH)
    client_side.database.create_database()