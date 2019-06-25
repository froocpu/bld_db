from ..domain.notation import Notation
from parse.exceptions import AmbiguousStatementException, BadSeparatorException, BadMultiplierException
from .string import count_occurrences


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
    TODO: handle ([M',U2])*2?
    """
    empty = ""
    if m not in string:
        return string.replace(op, empty).replace(cp, empty)

    splits = string.split(m)
    try:
        n = int(splits[1])
        cleaned = splits[0].replace(op, empty).replace(cp, empty)
        if n <= 0 or n > 10 or len(splits) != 2:
            raise BadMultiplierException("Multiplier character '{}' provided is invalid.".format(m))
        return cleaned * n
    except IndexError:
        print("Could not split using the multiplier provided.")