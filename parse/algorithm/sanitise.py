from .config import Notation


def sanitise(s):
    """
    A function for performing string sanitation.
    Sanitation is not the same as validation - some characters may be acceptable for sanisation, but not for validation.
    TODO: should this be the case?
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
            sanitized = sanitized.replace(char, "")

    return sanitized
