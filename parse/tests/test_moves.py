import unittest

from parse.algorithm.moves import Move


class TestMoveClass(unittest.TestCase):
    def test_inverse(self):
        test_moves = ["U", "L2", "R'", "D'", "B2'", "d", "Lw", "R"]
        expected_moves = ["U'", "L2", "R", "D", "B2", "d'", "Lw'", "R'"]
        for i, move in enumerate(test_moves):
            this_move = Move(move)
            self.assertEqual(this_move.invert(), expected_moves[i])

    def test_SiGN(self):
        test_moves = ["Uw", "l2", "Rw'", "Dw'", "b2'", "Dw", "Lw", "Fw2", "U"]
        expected_moves = ["u", "l2", "r'", "d'", "b2'", "d", "l", "f2", "U"]
        for i, move in enumerate(test_moves):
            this_move = Move(move)
            self.assertEqual(this_move.to_SiGN(), expected_moves[i])
