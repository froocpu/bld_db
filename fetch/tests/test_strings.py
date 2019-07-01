import unittest
from ..etl.strings import rotate_sticker, signature
import numpy as np


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

    def test_signature(self):
        """
        When a numpy array is provided to signature()...
        Then a condensed string will be returned representing the values of that array.
        """
        sig_arr = np.array([[0, 1, 1], [1, 2, 3]])
        sig_str = signature(sig_arr)
        self.assertTrue(isinstance(sig_str, str))
        self.assertEqual(sig_str, "011123")
