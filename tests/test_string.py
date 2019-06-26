import unittest
from parse.utils import count_occurrences


class TestUtils(unittest.TestCase):

    def test_count_occurrences_single_char(self):
        test_string = "Famous rice pudding recipe."
        test_string_alg = "R U R' U' R' F R2 U' R' U' R U R' F'"
        self.assertEqual(count_occurrences("r", test_string), 2)
        self.assertEqual(count_occurrences("'", test_string_alg), 8)
        self.assertEqual(count_occurrences(" ", test_string_alg), 13)

    def test_count_occurrences_multiple_chars(self):
        test_string = "speedcubin'?"
        test_string_alg = "Lw' U2 R U2 Lw U2 Lw' U2 R' U2 Lw U2"
        self.assertEqual(count_occurrences("ee", test_string), 1)
        self.assertEqual(count_occurrences("Lw", test_string_alg), 4)
        self.assertEqual(count_occurrences("Lw'", test_string_alg), 2)