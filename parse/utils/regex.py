import re

from ..domain.notation import Notation


class Regex:

    def __init__(self):
        p = ''.join([
            "\\" + Notation.PRIME,
            "\\" + Notation.WIDE,
            "\\" + Notation.PAUSE,
            "\\" + Notation.CONJUGATE,
            "\\" + Notation.COMMUTATOR,
            Notation.BLOCKS,
            Notation.SLICES,
            Notation.ROTATIONS
        ])
        self.pattern = "\[[{0}]*\]".format(p)

    def match_sequence(self, s):
        """
        Using the pre-generated pattern, find matches in a string.
        This will look for contents inside square brackets - the lowest nested brackets it can find.
        :param s: str
        :return: str
        """
        match = re.search(self.pattern, s)
        if match is None:
            return None
        return match.group(0)