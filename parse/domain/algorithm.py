import re

from .moves import Move, BaseMove
from .config import Notation
from .sanitise import sanitise
from parse.utils import split_sequence, clean_alg, split_ab, parse_brackets, multiplier


class Algorithm(BaseMove):

    def __init__(self, s):
        self.raw = s
        # Remove whitespace and any 'illegal' characters from the raw string.
        cleaned = sanitise(clean_alg(s))

        # Scan the cleaned string for instances of (A)*n, where A needs to be repeated n times.
        # Expand each match and reset the string.
        multiplier_pattern_matches = list(set(re.findall(Notation.MULTIPLIER_REGEX, cleaned)))

        for m in multiplier_pattern_matches:
            expanded_expression = multiplier(m)
            cleaned = cleaned.replace(m, expanded_expression)

        # Presumably, at this point, brackets don't mean anything significant, so remove them.
        cleaned = cleaned.replace(Notation.EXPRESSION_OB, Notation.EMPTY).replace(Notation.EXPRESSION_CB, Notation.EMPTY)

        # Scan the alg for occurrences of conjugates and commutators. Sort them by their depth.
        # If there aren't any, simply finish processing the alg.
        inner_algs = sorted(list(parse_brackets(cleaned)))

        if len(inner_algs) == 0:
            tidy = handle_edge_case(cleaned)
            cleaned = expand_algorithm(tidy)
        else:
            this_depth = inner_algs[-1][0]
            # Starting with the deepest matches, start expanding out the ald and resetting the parsed alg.
            while len(inner_algs) > 0:
                if inner_algs[-1][0] != this_depth and this_depth > 0:
                    # Overwrite the original list of inner algs, else the str.replace() call won't find a match.
                    inner_algs = sorted(list(parse_brackets(cleaned)))
                original = inner_algs.pop()[1]
                replacement = handle_edge_case(original)
                ab = expand_algorithm(replacement)
                cleaned = cleaned.replace("[" + original + "]", ab)

        # Once there are no more work to do, split the final string into individual move objects.
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


def handle_edge_case(s):
    """
    Handle the specific edge case, where brackets are omitted from the sequence [A:B,C]
    TODO: this might not be necessary.
    :param s: string with algorithm
    :return:
    """
    if Notation.CONJUGATE in s and Notation.COMMUTATOR in s:
        split = s.split(Notation.CONJUGATE)
        parsed = [expand_algorithm(i) for i in split]
        return parsed[0] + ":" + parsed[1]
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


