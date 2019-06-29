class Notation:
    """
    https://www.worldcubeassociation.org/regulations/#article-12-notation

    TODO: alternate notation for rotations
    12a4a) Clockwise, 90 degrees: [f] or z, [b] or z', [r] or x, [l] or x', [u] or y, [d] or y'.
    12a4b) Counter-clockwise, 90 degrees: [f'] or z', [b'] or z, [r'] or x', [l'] or x, [u'] or y', [d'] or y.
    12a4c) 180 degrees: [f2] or z2, [b2] or z2, [r2] or x2, [l2] or x2, [u2] or y2, [d2] or y2.
    """
    WIDE = 'w'
    PRIME = "'"
    DOUBLE = '2'
    PAUSE = '.'
    # Define rotations and which face they should follow.
    ROTATIONS = 'xyz'
    ROTATION_FOLLOWS_R = ROTATIONS[0]
    ROTATION_FOLLOWS_U = ROTATIONS[1]
    ROTATION_FOLLOWS_F = ROTATIONS[2]
    # Define slices, and the rules on which face the slice move should follow.
    SLICES = 'MES'
    SLICE_FOLLOWS_L = SLICES[0]
    SLICE_FOLLOWS_F = SLICES[2]
    SLICE_FOLLOWS_D = SLICES[1]
    # Define face turns and which one denotes which cube side.
    BLOCKS = 'UDFBRL'
    UP_FACE_CHAR = BLOCKS[0]
    DOWN_FACE_CHAR = BLOCKS[1]
    FRONT_FACE_CHAR = BLOCKS[2]
    BACK_FACE_CHAR = BLOCKS[3]
    RIGHT_FACE_CHAR = BLOCKS[4]
    LEFT_FACE_CHAR = BLOCKS[5]
    # Define other syntax
    CONJUGATE = ':'
    COMMUTATOR = ','
    MULTIPLIER = '*'
    COMM_CONJ_OB = '['
    COMM_CONJ_CB = ']'
    EXPRESSION_OB = '('
    EXPRESSION_CB = ')'
    MULTIPLIER_REGEX = r'\([A-Z\'0-9]+\)\*[0-9]+'
    EMPTY = ''


class Validation:
    MOVE_MAX_CHAR_LENGTH = 3
    MULTIPLIER_MIN_REPITITIONS = 0
    MULTIPLIER_MAX_REPITITIONS = 10
    ALG_CHAR_MAX_LENGTH = 100  # arbitrary
    ALG_CHAR_MIN_LENGTH = 4  # it would exclude references to UFR, UBL etc when parsing a sheet.