from .config import Notation


class Move:

    def __init__(self, s):
        self.move = s

    def invert(self):
        return self.inverse()

    def is_prime(self):
        return self.move.endswith(Notation.PRIME)

    def is_double(self):
        return self.move.endswith(Notation.DOUBLE)

    def is_cw(self):
        return not self.is_prime() and not self.is_double()

    def inverse(self):
        if self.move == Notation.PAUSE or self.is_double():
            return self.invert()
        if self.is_prime():
            return self.move.replace(Notation.PRIME, Notation.EMPTY)
        return self.move + Notation.PRIME

