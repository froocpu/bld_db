from .validation import validate_move
from .notation import Notation


class BaseMove:

    @staticmethod
    def inverse(move):
        if move == Notation.PAUSE or move.endswith(Notation.DOUBLE):
            return move
        if move.endswith(Notation.PRIME):
            return move.replace(Notation.PRIME, "")
        return move + Notation.PRIME

    @staticmethod
    def SiGN(move):
        if Notation.WIDE in move:
            rm_wide = move.replace(Notation.WIDE, "")
            return rm_wide[0].lower() + rm_wide[1:]
        return move

    @staticmethod
    def wca(move):
        if Notation.WIDE not in move:
            add_wide = move[0].upper() + Notation.WIDE + move[1:]
            return add_wide
        return move


class Move(BaseMove):

    def __init__(self, s):
        self.move = validate_move(s)

    def invert(self):
        return self.inverse(self.move)

    def to_SiGN(self):
        return self.SiGN(self.move)

    def to_wca(self):
        return self.wca(self.move)
