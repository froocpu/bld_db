import re

from .moves import Move, BaseMove
from .notation import Notation
from .sanitise import sanitise
from parse.utils import split_sequence, clean_alg, split_ab, parse_brackets, multiplier


class Algorithm(BaseMove):

    def __init__(self, s):
        self.raw = s

        cleaned = sanitise(clean_alg(s))

        matches = list(set(re.findall(r'\([A-Z\'0-9]+\)\*[0-9]+', cleaned)))

        while len(matches) > 0:
            x = matches.pop()
            y = multiplier(x)
            cleaned = cleaned.replace(x, y)

        subparts = sorted(list(parse_brackets(cleaned)))

        if len(subparts) == 0:
            tidy = normalise(cleaned)
            alg = expand_algorithm(tidy)
            self.moves = [Move(m) for m in split_sequence(alg)]
        else:
            this_depth = subparts[-1][0]

            while len(subparts) > 0:
                if subparts[-1][0] != this_depth and this_depth > 0:
                    subparts = sorted(list(parse_brackets(cleaned)))
                original_subpart = subparts.pop()[1]
                this_subpart = normalise(original_subpart)
                ab = expand_algorithm(this_subpart)
                cleaned = cleaned.replace("[" + original_subpart + "]", ab)

            self.moves = [Move(m) for m in split_sequence(cleaned)]

    def alg(self):
        return [m.move for m in self.moves]

    def invert(self):
        moves = [self.inverse(m.move) for m in self.moves]
        moves.reverse()
        return moves

    def convert_sign(self):
        return [self.SiGN(m.move) for m in self.moves]

    def convert_wca(self):
        return [self.wca(m.move) for m in self.moves]


def expand_algorithm(s):
    """
    Until I know where to put this, this will take a raw string and split it into A and B components.
    :param s: raw algorithm.
    :return: str - expanded algorithm
    TODO: remove repeated code.
    TODO: process nested brackets.
    """
    if Notation.COMMUTATOR in s:
        sep = Notation.COMMUTATOR
    elif Notation.CONJUGATE in s:
        sep = Notation.CONJUGATE
    else:
        multiplied = multiplier(s)
        move_objects = [Move(m) for m in split_sequence(multiplied)]
        return ''.join(constructor(a=move_objects))

    A, B = split_ab(s, sep)

    A = multiplier(A)
    B = multiplier(B)

    A = [Move(m) for m in split_sequence(A)]
    B = [Move(m) for m in split_sequence(B)]

    comm = (constructor(A, B, 1) if sep == Notation.COMMUTATOR else constructor(A, B, 2))
    return ''.join(comm)


def normalise(s):
    """
    Handle the specific edge case, where brackets are omitted from the sequence [A:B,C]
    :param s: string with algorithm
    :return:
    """
    if Notation.CONJUGATE in s and Notation.COMMUTATOR in s:
        split_subparts = s.split(Notation.CONJUGATE)
        parsed_subparts = [expand_algorithm(i) for i in split_subparts]
        return parsed_subparts[0] + ":" + parsed_subparts[1]
    return s


def constructor(a, b=None, alg_type=0):
    """
    Logic for constructing a commutator (A B A' B'), a conjugate (A B A') or a simple sequence of moves.
    :param a: list of Move objects.
    :param b: list of Move objects.
    :param alg_type: commutator (1), conjugate (2) or neither (0).
    :type alg_type: int
    :return: list of strings.
    """

    A = [m.move for m in a]

    if alg_type == 0 or b is None:
        return A

    B = [m.move for m in b]

    Ai = [m.invert() for m in a]
    Ai.reverse()

    base = A + B + Ai

    if alg_type == 1:
        Bi = [m.invert() for m in b]
        Bi.reverse()
        return base + Bi
    if alg_type == 2:
        return base
    else:
        return None


