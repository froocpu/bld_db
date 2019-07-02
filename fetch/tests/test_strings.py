import unittest
import numpy as np

from ..etl.strings import signature


class TestStrings(unittest.TestCase):

    def test_signature(self):
        """
        When a numpy array is provided to signature()...
        Then a condensed string will be returned representing the values of that array.
        """
        sig_arr = np.array([[0, 1, 1], [1, 2, 3]])
        sig_str = signature(sig_arr)
        self.assertTrue(isinstance(sig_str, str))
        self.assertEqual(sig_str, "011123")

