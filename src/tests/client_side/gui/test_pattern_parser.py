import unittest

from OpenDrive.client_side.gui.explorer import pattern_parser


class TestFileExtensions(unittest.TestCase):

    def test_parse_file_extensions(self):
        in_string = "/file.txt, *.txt, /folder1/*.tmp"
        print(pattern_parser.parse_patterns(in_string))
