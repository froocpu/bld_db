from .moves import Move, BaseMove
from .notation import Notation
from parse.utils import split_sequence, clean_alg
from parse.exceptions import BadMultiplierException


class Algorithm(BaseMove):

    def __init__(self, s):
        self.raw = s
        clean = clean_alg(s)
        self.moves = [Move(m) for m in split_sequence(clean)]

    def invert(self):
        moves = [self.inverse(m.move) for m in self.moves]
        moves.reverse()
        return moves

    def to_SiGN(self):
        return [self.SiGN(m.move) for m in self.moves]

    def toWca(self):
        return [self.wca(m.move) for m in self.moves]


def constructor(a, b, alg_type=0):
    """
    Logic for constructing a commutator (A B A' B') or a conjugate (A B A')
    :param a: list of Move objects.
    :param b: list of Move objects.
    :param alg_type: commutator (0) or conjugate (1)
    :type alg_type: int
    :return: list of strings.
    """
    A = [m.move for m in a]
    B = [m.move for m in b]
    Ai = [m.invert() for m in a]
    Ai.reverse()
    base = A + B + Ai
    if alg_type == 0:
        Bi = [m.invert() for m in b]
        Bi.reverse()
        return base + Bi
    if alg_type == 1:
        return base
    else:
        return None


def parse_brackets(string, ob="[", cb="]"):
    """
    Generate parenthesized contents in string as pairs (level, contents).
    https://stackoverflow.com/questions/4284991/parsing-nested-parentheses-in-python-grab-content-by-level
    :param string: cuber algorithm, concise notation.
    :type string: str
    :param ob: open bracket, the symbol to denote an starting point for the string. Usually '[' or '('.
    :type ob: str
    :param cb: closed bracket, the symbol to denote an ending point for the string. Usually ']' or ')'.
    :type cb: str
    :return: str
    """
    stack = []
    for i, c in enumerate(string):
        if c == ob:
            stack.append(i)
        elif c == cb and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])


def multiplier(string, m=Notation.MULTIPLIER, op='(', cp=')'):
    """
    Parse parentheses and replicate it n times according to its multiplier, if one exists.
    :param string: raw algorithm
    :type string: str
    :param op: open parenthesis - symbol to denote the opener.
    :type op: str
    :param cp: closed parenthesis - symbol to denote the closer.
    :type cp: str
    :param m: the symbol to denote the multiplier
    :type m: str
    :return: str
    """
    empty = ""

    if m not in string:
        raise BadMultiplierException("Multiplier character is missing.")
    splits = string.split(m)
    try:
        n = int(splits[1])
        cleaned = splits[0].replace(op, empty).replace(cp, empty)
        if n <= 0 or n > 10 or len(splits) != 2:
            raise BadMultiplierException("Multiplier character '{}' provided is invalid.".format(m))
        return cleaned * n
    except IndexError:
        print("Could not split using the multiplier provided.")
