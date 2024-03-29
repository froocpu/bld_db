from .config import Notation
from parse.exceptions import IllegalCharactersException


def sanitise(s):
    """
    A function for performing string sanitation.
    Sanitation is not the same as validation - some characters may be acceptable for sanisation, but not for validation.
    :param s: raw algorithm string
    :type s: str
    :return: str
    """
    n = Notation()
    legal_chars = ''.join(sorted([
        n.COMMUTATOR,
        n.CONJUGATE,
        n.MULTIPLIER,
        n.PRIME,
        n.BLOCKS,
        n.BLOCKS.lower(),
        n.PAUSE,
        n.SLICES,
        n.SLICES.lower(),
        n.WIDE,
        n.WIDE.upper(),
        n.ROTATIONS,
        n.ROTATIONS.upper(),
        n.COMM_CONJ_CB,
        n.COMM_CONJ_OB,
        n.EXPRESSION_CB,
        n.EXPRESSION_OB,
        "1234567890"
    ]))
    sanitized = s
    for char in "".join(set(s)):
        if char not in legal_chars:
            # TODO: vectorise this, i.e. not run for each string.
            raise IllegalCharactersException("Contains characters that don't correspond to anything in cubing notation.")

    return sanitized
