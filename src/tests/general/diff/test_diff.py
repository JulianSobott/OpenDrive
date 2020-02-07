import unittest

from OpenDrive.general.diff import *


class TestEditDistance(unittest.TestCase):

    def test_equal_texts(self):
        text1 = "Hello"
        text2 = "Hello"
        diff = edit_distance(text1, text2)
        self.assertEqual(0, diff)

    def test_empty_texts(self):
        text1 = ""
        text2 = ""
        diff = edit_distance(text1, text2)
        self.assertEqual(0, diff)

    def test_one_empty_text(self):
        text1 = "Hello"
        text2 = ""
        diff = edit_distance(text1, text2)
        self.assertEqual(len(text1), diff)

    def test_different1(self):
        text1 = "ABDCE"
        text2 = "ABCD"
        diff = edit_distance(text1, text2)
        self.assertEqual(2, diff)


class TestOperations(unittest.TestCase):

    def test_equal(self):
        text1 = "H"
        text2 = "H"
        ops = diff_operations(text1, text2)
        self.assertEqual(0, len(ops))

    def test_bot_equal_1(self):
        text1 = "H"
        text2 = ""
        ops = diff_operations(text1, text2)
        expected = [Operation(INSERT_AFTER, 0, 0, "H")]
        self.assertEqual(expected, ops)


if __name__ == '__main__':
    unittest.main()
