import unittest
import os
import shutil

from client_side import database, paths
from general.database import delete_db_file
from src.tests.Logging import logger


class TestFileChange(unittest.TestCase):
    abs_folder_path = os.path.join(paths.PROJECT_PATH, "local/client_side/dummy_folder/")

    def setUp(self):
        delete_db_file(paths.LOCAL_DB_PATH)
        database.create_database()
        logger.debug(self.abs_folder_path)
        os.mkdir(self.abs_folder_path)
        database.SyncFolder.create(self.abs_folder_path)

    def tearDown(self):
        shutil.rmtree(self.abs_folder_path, ignore_errors=True)

    def test_create_file(self):
        pass

if __name__ == '__main__':
    unittest.main()
