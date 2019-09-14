import unittest
from parse.utils.string import count_occurrences, clean_alg


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

    def test_clean_alg(self):

        expected = "RDS"

        alg_single_spaced = "R D S"
        alg_leading_ws = "   RDS"
        alg_trailing_ws = "RDS   "
        alg_all_ws = "\t  R \t D \r       S\n"
        alg_unicode = "RDS\xe5"
        alg_non_alphanumeric = "[L,R] R D S . (R' D' S')*100 [M:B]"
        alg_fancy_single_quote = "R U R\u2019 U\u2019"

        self.assertEqual(clean_alg(alg_single_spaced), expected)
        self.assertEqual(clean_alg(alg_leading_ws), expected)
        self.assertEqual(clean_alg(alg_trailing_ws), expected)
        self.assertEqual(clean_alg(alg_all_ws), expected)
        self.assertEqual(clean_alg(alg_unicode), expected)

        self.assertEqual(clean_alg(alg_non_alphanumeric), "[L,R]RDS.(R'D'S')*100[M:B]")
        self.assertEqual(clean_alg(alg_fancy_single_quote), "RUR'U'")
