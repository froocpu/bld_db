import re

from .config import Notation, Validation
from .moves import Move, BaseMove
from .config import Notation
from .sanitise import sanitise
from parse.utils import clean_alg, count_occurrences
from parse.exceptions import BadMultiplierException, BadSeparatorException, AmbiguousStatementException, EmptyAlgorithmException


class Algorithm(BaseMove):

    def __init__(self, s):
        # Throw some early exceptions.
        if s is None or s == Notation.EMPTY:
            raise EmptyAlgorithmException("Alg is either completely empty at initialisation, or just missing.")

        self.raw = s
        # Remove whitespace and any 'illegal' characters from the raw string.
        cleaned = sanitise(clean_alg(s))
        self.cleaned = cleaned

        # Scan the cleaned string for instances of (A)*n, where A needs to be repeated n times.
        # Expand each match and reset the string.
        multiplier_pattern_matches = list(set(re.findall(Notation.MULTIPLIER_REGEX, cleaned)))

        for m in multiplier_pattern_matches:
            expanded_expression = multiplier(m)
            cleaned = cleaned.replace(m, expanded_expression)

        # If there are still multiplier symbols present, then raise an exception.
        if Notation.MULTIPLIER in cleaned:
            raise BadMultiplierException("Regex did not replace the multiplier statements, probably due to an invalid number of iterations specified.".format(cleaned))

        # Presumably, at this point, brackets don't mean anything significant, so remove them.
        cleaned = cleaned.replace(Notation.EXPRESSION_OB, Notation.EMPTY).replace(Notation.EXPRESSION_CB, Notation.EMPTY)

        # Scan the alg for occurrences of conjugates and commutators. Sort them by their depth.
        # If there aren't any, simply finish processing the alg.
        inner_algs = sorted(list(parse_brackets(cleaned)))
        self.alg_depth = len(inner_algs)

        if len(inner_algs) == 0:
            tidy = handle_bracketless_statement(cleaned)
            cleaned = expand_algorithm(tidy)
        else:
            this_depth = inner_algs[-1][0]
            # Starting with the deepest matches, start expanding out the ald and resetting the parsed alg.
            while len(inner_algs) > 0:
                if inner_algs[-1][0] != this_depth and this_depth > 0:
                    # Overwrite the original list of inner algs, else the str.replace() call won't find a match.
                    inner_algs = sorted(list(parse_brackets(cleaned)))
                original = inner_algs.pop()[1]
                replacement = handle_bracketless_statement(original)
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
        move_objects = [Move(m) for m in split_sequence(s)]
        return ''.join(constructor(a=move_objects))

    A, B = split_ab(s, sep)

    A = [Move(m) for m in split_sequence(A)]
    B = [Move(m) for m in split_sequence(B)]

    comm = (constructor(A, B, 1) if sep == Notation.COMMUTATOR else constructor(A, B, 2))
    return ''.join(comm)


def handle_bracketless_statement(s):
    """
    Handles the case where brackets are omitted from the sequence [A:B,C]
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

    if a is None or len(a) == 0:
        raise EmptyAlgorithmException("No moves detected in this algorithm.")
    if (b is None or len(b) == 0) and alg_type > 0:
        raise EmptyAlgorithmException("This algorithm expected moves in the B part, but none were detected.")

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


def split_sequence(s):
    """
    Parse a string into a list of moves to validate according to WCA and SiGN notation.
    :param s: str
    :return: str
    """
    size = len(s)
    if size == 1:
        return s
    size -= 1
    moves = []
    counter = 0
    while counter <= size:
        this_move = s[counter]
        # If the next character in the sequence matches these, then append it to the move and increment the counter.
        # Must be done in this order.
        for ch in [Notation.WIDE, Notation.DOUBLE, Notation.PRIME]:
            if counter+1 > size:
                break
            if s[counter+1] == ch:
                this_move += s[counter+1]
                counter += 1
        moves.append(this_move)
        counter += 1
    return moves


def split_ab(s, sep):
    """
    Take a simple sequence and split it into an A and B part. Assumes that the statement is simple.
    :param s: original string.
    :param sep: the separator character. Use a comma for commutators and a colon for conjugates.
    :return: objects
    """
    if sep not in [Notation.COMMUTATOR, Notation.CONJUGATE]:
        raise BadSeparatorException("This alg uses non-standard notation - '{0}' is not allowed.".format(sep))
    if count_occurrences(sep, s) != 1:
        raise AmbiguousStatementException("This statement appears to have incorrect syntax. '{0}'".format(s))

    return s.split(sep)


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


def multiplier(string):
    """
    Parse parentheses and replicate it n times according to its multiplier, if one exists.
    :param string: raw algorithm
    :type string: str
    :return: str
    TODO: handle ([M',U2])*2?
    """
    splits = string.split(Notation.MULTIPLIER)
    try:
        n = int(splits[1])
        cleaned = splits[0].replace(Notation.EXPRESSION_OB, Notation.EMPTY)\
            .replace(Notation.EXPRESSION_OB, Notation.EMPTY)
        if n < Validation.MULTIPLIER_MIN_REPITITIONS or n > Validation.MULTIPLIER_MAX_REPITITIONS or len(splits) != 2:
            raise BadMultiplierException("Multiplier statement '{}' provided is invalid or illegal.".format(splits[0]))
        return cleaned * n
    except IndexError:
        print("Could not split using the multiplier statement provided: {}".format(splits[0]))
