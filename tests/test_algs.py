import unittest

from parse.utils import split_sequence
from parse.domain import Algorithm, Move
from parse.domain import constructor


class TestMoveClass(unittest.TestCase):

    def test_split_ab_good(self):
        good_comm = "U,R"
        good_conj = "U:R"
        pass

    def test_split_ab_bad(self):
        bad_comm = "U;R"
        bad_conj = "U,R,L"
        pass

    def test_split_sequence_long(self):
        seq = "ULwUw'U2l2L'Lw2'F"
        expected = ["U", "Lw", "Uw'", "U2", "l2", "L'", "Lw2'", "F"]
        split = split_sequence(seq)
        self.assertListEqual(split, expected)

    def test_invert_sexy(self):
        alg = Algorithm("R U R' U'")
        expected = ["U", "R", "U'", "R'"]
        self.assertListEqual(alg.invert(), expected)

    def test_invert_tperm(self):
        t = Algorithm("R U R' U' R' F R2 U' R' U' R U R' F'")
        expected = ["F", "R", "U'", "R'", "U", "R", "U", "R2'", "F'", "R", "U", "R", "U'", "R'"]
        self.assertListEqual(t.invert(), expected)

    def test_construct_commutator(self):
        comm = constructor([Move("R")], [Move("U")])
        expected = ["R", "U", "R'", "U'"]
        self.assertListEqual(comm, expected)