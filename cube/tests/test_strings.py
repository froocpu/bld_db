import unittest
from ..utils.strings import rotate_sticker


class TestStrings(unittest.TestCase):

    def test_rotate_sticker(self):
        """
        Given that an edge string has a length of two...
        When an edge string is passed to rotate_sticker...
        Then a reversed string will be returned.

        Given that a corner string has a length of three...
        And the CW flag is provided...
        When rotate_sticker is called...
        Then each character will be shifted one position to the left or right.
        """
        good_edge = "BU"
        good_corner = "ULF"
        bad_str_long = "adsf"
        bad_str_short = "A"

        self.assertEqual(rotate_sticker(good_edge), "UB")
        self.assertEqual(rotate_sticker(good_corner, cw=True), "LFU")
        self.assertEqual(rotate_sticker(good_corner, cw=False), "FUL")
        self.assertIsNone(rotate_sticker(bad_str_short))
        self.assertIsNone(rotate_sticker(bad_str_long))
