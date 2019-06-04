import unittest

from OpenDrive.client_side.gui.explorer import pattern_parser


class TestFileExtensions(unittest.TestCase):

    def test_parse_file_extensions(self):
        in_string = ".txt, .py, .test.ext"
        expected = [".txt", ".py", ".test.ext"]

