import unittest
from parse.domain import sanitise


class TestSanitise(unittest.TestCase):

    def test_sanitise_clean(self):
        string = "RUR'U'."
        self.assertEqual(sanitise(string), string)

    def test_sanitise_clean_varied_characters(self):
        string = "xMD[R,U]UR'U'z(M).*4[S:U]y"
        self.assertEqual(sanitise(string), string)

    def test_sanitise_illegal_chars(self):
        expected = "RUR'U'"
        bad_strings = ["RUpooR'U'", "!R&U£R<'U\\'", "RUR'?U'", "aRiIUkhqvjR'U'\""]
        for bs in bad_strings:
            self.assertEqual(sanitise(bs), expected)
