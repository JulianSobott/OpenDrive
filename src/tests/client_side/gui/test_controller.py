import unittest
import time

from OpenDrive.client_side import gui


class TestController(unittest.TestCase):

    @unittest.skip
    def test_procedure(self):
        gui.open_gui()
        time.sleep(2)
        gui.close_gui()
        time.sleep(2)
        gui.open_gui()
        time.sleep(2)
        gui.stop()
