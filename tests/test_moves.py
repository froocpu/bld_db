import unittest

from parse.domain import Move
from parse.exceptions import InvalidMoveException


class TestMoveClass(unittest.TestCase):

    def test_move_init_good(self):
        good_moves = ["Uw", "L'", "r", "D2", ".", "S'", "x"]
        for move in good_moves:
            this_move = Move(move)
            self.assertEqual(this_move.move, move)

    def test_move_init_bad(self):
        bad_moves = ["Sw2", "s2'", "X", "L'2", "D'2", "uw'2", "lw"]
        for move in bad_moves:
            with self.assertRaises(InvalidMoveException):
                Move(move)

    def test_inverse(self):
        test_moves = ["U", "L2", "R'", "D'", "B2'", "d", "Lw", "R"]
        expected_moves = ["U'", "L2'", "R", "D", "B2", "d'", "Lw'", "R'"]
        for i, move in enumerate(test_moves):
            this_move = Move(move)
            self.assertEqual(this_move.invert(), expected_moves[i])

    def test_SiGN(self):
        test_moves = ["Uw", "l2", "Rw'", "Dw'", "b2'", "Dw", "Lw", "Fw2", "U"]
        expected_moves = ["u", "l2", "r'", "d'", "b2'", "d", "l", "f2", "U"]
        for i, move in enumerate(test_moves):
            this_move = Move(move)
            self.assertEqual(this_move.to_SiGN(), expected_moves[i])