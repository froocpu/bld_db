from parse.domain.notation import Notation
from parse.exceptions import AmbiguousStatementException, BadSeparatorException
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
            # TODO: this isn't nice.
            #  A solution where a single string is indexed and updated would be better than using size counters.
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


