import unittest

from parse.domain import Algorithm


class TestAlgorithm(unittest.TestCase):

    alg_list = [

        "[R,U] R' F R2 U' [R': U'] U R' F'", # t-perm
        "[[M', U],[R D' R' D, F2]]",  # commutator
        "[U R U': M2][U' R' U: M2]",  # M2 method
        "[L: (U M' U M)*2]",  # multiplier
        "RUR'U'", # nothing required.
        "[U : R U R', D]", # cleaner
        "U : R U R', D",  # even cleaner
        "(M' U M U)*2",  # just a multiplier
        "M' U' (M' D')*2 U M'",  # in the middle of a subpart
        "M U' (M U) M U",  # nested
        "[S, R2]",  # throw in some S's
        "[U R': [E, R2]]",  # test Es
        "U"  # one move
        ]

    def test_tperm_simple(self):
        t = Algorithm("R U R' U' R' F R2 U' R' U' R U R' F'")
        expected = ["R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'", "R", "U", "R'", "F'"]
        expected_inverse = ["F", "R", "U'", "R'", "U", "R", "U", "R2'", "F'", "R", "U", "R", "U'", "R'"]
        self.assertListEqual(t.moves(), expected)
        self.assertListEqual(t.invert(), expected_inverse)



    def test_invert_sexy(self):
        alg = Algorithm("R U R' U'")
        expected = ["U", "R", "U'", "R'"]
        self.assertListEqual(alg.invert(), expected)


