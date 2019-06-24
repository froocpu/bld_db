from .moves import Move, BaseMove
from parse.utils import split_sequence, clean_alg


def construct_commutator(a, b):
    """
    Logic for constructing a commutator. A B A' B'.
    :param a: list of Move objects.
    :param b: list of Move objects.
    :return: list of strings.
    """
    A = [m.move for m in a]
    B = [m.move for m in b]
    Ai = [m.invert() for m in a]
    Bi = [m.invert() for m in b]
    Ai.reverse()
    Bi.reverse()

    return A + B + Ai + Bi


def construct_conjugate(a, b):
    """
    Logic for constructing a conjugate. A B A'.
    :param a: list of Move objects.
    :param b: list of Move objects.
    :return: list of strings.
    """
    A = [m.move for m in a]
    B = [m.move for m in b]
    Ai = [m.invert() for m in a]
    Ai.reverse()
    return A + B + Ai


class Algorithm(BaseMove):

    def __init__(self, s):
        self.raw = s
        clean = clean_alg(s)
        self.moves = [Move(m) for m in split_sequence(clean)]

    # TODO: Is this the best implementation?
    def invert(self):
        moves = [self.inverse(m.move) for m in self.moves]
        moves.reverse()
        return moves

    def to_SiGN(self):
        return [self.SiGN(m.move) for m in self.moves]

    def toWca(self):
        return [self.wca(m.move) for m in self.moves]
