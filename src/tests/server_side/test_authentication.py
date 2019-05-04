import datetime
import unittest
import uuid
import shutil
from typing import Tuple
import os

from OpenDrive.server_side import database, paths, authentication
from OpenDrive.general.database import delete_db_file
from OpenDrive.server_side import server_json as server_json
from OpenDrive.server_side.database import Token
from tests.server_side.helper_server import h_deactivate_set_user_authenticated, \
    h_register_dummy_user_device, h_clear_init_server_folders, h_register_dummy_user
from tests.server_side.database import h_setup_server_database
from tests.od_logging import logger


class TestRegistration(unittest.TestCase):

    def setUp(self):
        h_clear_init_server_folders()
        h_setup_server_database()

    def tearDown(self) -> None:
        pass

    @h_deactivate_set_user_authenticated
    def test_add_update_device_new(self):
        user = h_register_dummy_user()
        mac = str(uuid.getnode())
        authentication._add_update_device(user.user_id, mac)
        all_devices = database.Device.get_all()
        self.assertEqual(1, len(all_devices))
        self.assertEqual(mac, all_devices[0].mac_address)
        json_path = server_json._get_file_path(user.user_id, 1)
        self.assertTrue(os.path.isfile(json_path))

    @h_deactivate_set_user_authenticated
    def test_add_update_device_expires(self):
        pass

    @h_deactivate_set_user_authenticated
    def test_add_update_device_existing(self):
        pass

    @h_deactivate_set_user_authenticated
    def test_register_user_device(self):
        username = "Anne"
        password = "2hj:_sAdf"
        email = None
        mac = str(uuid.getnode())
        token = authentication.register_user_device(username, password, mac, email)
        self.assertIsInstance(token, Token)
        all_devices = database.Device.get_all()
        self.assertEqual(1, len(all_devices))
        all_users = database.User.get_all()
        self.assertEqual(1, len(all_users))
        user = all_users[0]
        self.assertEqual(user, database.User(1, username, user.password, email))
        json_path = server_json._get_file_path(1, 1)
        self.assertTrue(os.path.isfile(json_path))

    @h_deactivate_set_user_authenticated
    def test_register_user_device_existing(self):
        username = "Anne"
        password = "2hj:_sAdf"
        email = None
        mac = str(uuid.getnode())
        token = authentication.register_user_device(username, password, mac, email)
        self.assertIsInstance(token, Token)
        token = authentication.register_user_device(username, password, mac, email)
        self.assertIsInstance(token, str)


class TestLogin(unittest.TestCase):

    def setUp(self):
        h_clear_init_server_folders()
        self.user, self.device, self.token = h_register_dummy_user_device()

    @h_deactivate_set_user_authenticated
    def test_login_manual_user_device(self):
        username = self.user.username
        password = self.user.password
        mac = self.device.mac_address
        token = authentication.login_manual_user_device(username, password, mac)
        self.assertIsInstance(token, Token)

    @h_deactivate_set_user_authenticated
    def test_login_auto(self):
        mac = self.device.mac_address
        ret = authentication.login_auto(self.token, mac)
        self.assertTrue(ret)


if __name__ == '__main__':
    unittest.main()
