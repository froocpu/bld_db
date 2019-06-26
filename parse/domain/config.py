class Notation:
    """
    https://www.worldcubeassociation.org/regulations/#article-12-notation

    TODO: alternate notation for rotations
    12a4a) Clockwise, 90 degrees: [f] or z, [b] or z', [r] or x, [l] or x', [u] or y, [d] or y'.
    12a4b) Counter-clockwise, 90 degrees: [f'] or z', [b'] or z, [r'] or x', [l'] or x, [u'] or y', [d'] or y.
    12a4c) 180 degrees: [f2] or z2, [b2] or z2, [r2] or x2, [l2] or x2, [u2] or y2, [d2] or y2.
    """
    WIDE = "w"
    PRIME = "'"
    DOUBLE = "2"
    PAUSE = "."
    ROTATIONS = 'xyz'
    SLICES = 'MES'
    BLOCKS = 'ULFRBD'
    CONJUGATE = ":"
    COMMUTATOR = ","
    MULTIPLIER = "*"
    COMM_CONJ_OB = "["
    COMM_CONJ_CB = "]"
    EXPRESSION_OB = "("
    EXPRESSION_CB = ")"
    MULTIPLIER_REGEX = r'\([A-Z\'0-9]+\)\*[0-9]+'
    EMPTY = ""


class Validation:
    MOVE_MAX_CHAR_LENGTH = 3