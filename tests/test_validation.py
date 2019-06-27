import unittest

from parse.domain.validation import validate_move, generate_valid_moves
from parse.exceptions.moves import InvalidMoveException


class TestValidate(unittest.TestCase):

    def setUp(self):
        self.validation_set = generate_valid_moves()

    def test_good_moves(self):
        good_moves = ['.',
                      'B', "B'", 'B2', "B2'", 'Bw', "Bw'", 'Bw2',
                      'D', "D'", 'D2', "D2'", 'Dw', "Dw'", 'Dw2',
                      'E', "E'", 'E2',
                      'F', "F'", 'F2', "F2'", 'Fw', "Fw'", 'Fw2',
                      'L', "L'", 'L2', "L2'", 'Lw', "Lw'", 'Lw2',
                      'M', "M'", 'M2',
                      'R', "R'", 'R2', "R2'", 'Rw', "Rw'", 'Rw2',
                      'S', "S'", 'S2',
                      'U', "U'", 'U2', "U2'", 'Uw', "Uw'", 'Uw2',
                      'b', "b'", 'b2', "b2'",
                      'd', "d'", 'd2', "d2'",
                      'e', "e'", 'e2', 'f', "f'", 'f2', "f2'",
                      'l', "l'", 'l2', "l2'",
                      'm', "m'", 'm2',
                      'r', "r'", 'r2', "r2'",
                      's', "s'", 's2',
                      'u', "u'", 'u2', "u2'",
                      'x', "x'", 'x2',
                      'y', "y'", 'y2',
                      'z', "z'", 'z2']

        for move in good_moves:
            self.assertEqual(validate_move(move, self.validation_set), move)

    def test_bad_moves(self):
        bad_letters = 'acghijknopqtvw'
        bad_moves = ["Sw2", "s2'", "X", "L'2", "D'2", "uw'2", "lw", "'Lw"]
        all_bad_moves = list(bad_letters) + list(bad_letters.upper()) + bad_moves
        for move in all_bad_moves:
            with self.assertRaises(InvalidMoveException):
                validate_move(move, self.validation_set)