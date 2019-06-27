from parse.exceptions import InvalidMoveException
from .config import Notation, Validation


def validate_move(s, validation_set):
    """
    Check whether the letter provided confirms to valid SiGN or WCA notation. Returns the original letter and the type.
    :param s: a string object denoting a single move.
    :type s: str
    :param validation_set: a set of moves to check against for validity.
    :type validation_set: tuple
    :return: str
    """
    move = s.strip()

    if len(move) > Validation.MOVE_MAX_CHAR_LENGTH:
        raise InvalidMoveException("'{0}' contains more than {1} characters.".format(move, Validation.MOVE_MAX_CHAR_LENGTH))

    if move not in validation_set:
        raise InvalidMoveException("'{0}' not a valid move in SiGN or WCA notation.".format(move))

    return move


def generate_valid_moves():
    """
    Generate all possible "valid" moves as a list from the AlgPart class.
    :return: tuple(str)
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

    return tuple(valid_moves)