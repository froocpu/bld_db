from parse.exceptions import InvalidMoveException
from .notation import Notation


def validate_move(s):
    """
    Check whether the letter provided confirms to valid SiGN or WCA notation. Returns the original letter and the type.
    :param s: str
    :return: str, str
    """
    move = s.strip()

    # TODO: make configurable.
    if len(move) > 3:
        raise InvalidMoveException("'{0}' contains more than three characters.".format(move))
    # TODO: Replace function call and point to a specific object for performance.
    # Simple string manipulations will have a negligible effect on performance, but this could be more elegant.
    if move not in generate_valid_moves():
        raise InvalidMoveException("'{0}' not a valid move in SiGN or WCA notation.".format(move))

    return move


def generate_valid_moves():
    """
    Generate all possible "valid" moves as a list from the AlgPart class.
    :return: list(str)
    """

    outer_turns = list(Notation.BLOCKS)
    slices = list(Notation.SLICES)
    wide_turns = list(Notation.BLOCKS.lower())
    rotations = list(Notation.ROTATIONS)
    small_slices = list(Notation.SLICES.lower())
    prime = Notation.PRIME
    double = Notation.DOUBLE
    wide = Notation.WIDE
    pause = Notation.PAUSE

    valid_moves = []

    for turn in wide_turns + outer_turns + slices + rotations + small_slices:
        valid_moves.append(turn)
        valid_moves.append(turn + prime)
        valid_moves.append(turn + double)
        if turn in outer_turns:
            valid_moves.append(turn + wide)
            valid_moves.append(turn + wide + double)
            valid_moves.append(turn + wide + prime)
            valid_moves.append(turn + double + prime)
        if turn in wide_turns:
            valid_moves.append(turn + double + prime)

    valid_moves.append(pause)

    return valid_moves