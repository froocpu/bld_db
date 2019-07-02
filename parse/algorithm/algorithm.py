import re

from .algorithm_helpers import expand_algorithm, handle_statement_no_brackets, split_sequence, parse_brackets, multiplier
from .config import Notation
from .moves import Move
from .sanitise import sanitise
from .validation import generate_valid_moves, validate_move

from ..utils import clean_alg, count_occurrences
from ..exceptions import *


class Algorithm:

    def __init__(self, s):

        # Check for errors early on.
        _raise_early_exceptions(s)

        # Begin
        self.raw = s

        # Remove whitespace and any 'illegal' characters from the raw string.
        cleaned = sanitise(clean_alg(s))

        # Scan the cleaned string for instances of (A)*n, where A needs to be repeated n times.
        # Expand each match and reset the string.
        multiplier_pattern_matches = list(set(re.findall(Notation.MULTIPLIER_REGEX, cleaned)))

        for m in multiplier_pattern_matches:
            expanded_expression = multiplier(m)
            cleaned = cleaned.replace(m, expanded_expression)

        # If there are still multiplier symbols present, then raise an exception.
        if Notation.MULTIPLIER in cleaned:
            raise BadMultiplierException(
                "Regex did not replace the multiplier statements, probably due to an invalid number of iterations specified."
                    .format(cleaned))

        # Presumably, at this point, brackets don't mean anything significant, so remove them.
        cleaned = cleaned.replace(Notation.EXPRESSION_OB, Notation.EMPTY).replace(Notation.EXPRESSION_CB, Notation.EMPTY)

        # Scan the alg for occurrences of conjugates and commutators. Sort them by their depth.
        # If there aren't any, simply finish processing the alg.
        inner_algs = sorted(list(parse_brackets(cleaned)))

        if len(inner_algs) == 0:
            tidy = handle_statement_no_brackets(cleaned)
            cleaned = expand_algorithm(tidy)
        else:
            this_depth = inner_algs[-1][0]
            # Starting with the deepest matches, start expanding out the ald and resetting the parsed alg.
            while len(inner_algs) > 0:
                if inner_algs[-1][0] != this_depth and this_depth > 0:
                    # Overwrite the original list of inner algs, else the str.replace() call won't find a match.
                    inner_algs = sorted(list(parse_brackets(cleaned)))
                original = inner_algs.pop()[1]
                replacement = handle_statement_no_brackets(original)
                ab = expand_algorithm(replacement)
                cleaned = cleaned.replace("[" + original + "]", ab)

        # Once the alg is expanded, split the final string into individual moves and validate them.
        validation_set = generate_valid_moves()
        validated_moves = [validate_move(m, validation_set) for m in split_sequence(cleaned)]

        # Create a Move instance for each move, provided they are all valid.
        self.moves = [Move(m) for m in validated_moves]

    def alg(self):
        return [m.move for m in self.moves]

    def invert(self):
        moves = [m.invert() for m in self.moves]
        moves.reverse()
        return moves

    def alg_cancelled(self):
        """
        Simple cancellation:
            Algorithm:
                - Scan two elements at a time and perform:
                    - If CW CW or CCW CCW, then replace both elements with a DOUBLE
                    - If CW CCW or CCW CW or DOUBLE DOUBLE, then remove both elements
                    - If CW DOUBLE or DOUBLE CW then replace both with CWW.
                    - If CCW DOUBLE or DOUBLE CCW then replace both with CW.
                -
        :return:
        """
        new_list = self.moves.copy()
        counter = 1
        while counter <= len(self.moves):
            change_flag = None
            x = self.moves[counter-1:counter+1]
            if x[0].is_cw() and x[1].is_cw():
                change_flag = True
                x.pop(0)
                x[1] = x[1].inverse()
            else:
                counter += 1


def _detect_unclosed_brackets(s, ob, cb):
    """
    A helper function to detect whether any any brackets exist that are unclosed.
    :param s: the string to check
    :type s: str
    :param ob: the type of open bracket to check
    :type ob: str
    :param cb: the type of closed bracket to check
    :type cb: str
    :return: None
    """
    count_ob = count_occurrences(ob, s)
    count_cb = count_occurrences(cb, s)

    if count_ob != count_cb:
        raise UnclosedBracketsException(
            "Unmatched brackets found: '{0}':{1}, '{2}':{3}".format(ob, count_ob, cb, count_cb))


def _raise_early_exceptions(s):
    """
    Perform initial checks and raise an exception early on before any significant work is done.
    :param s: string
    :type: s: str
    :return: str
    """
    # Throw some early exceptions.
    if s is None or s == Notation.EMPTY:
        raise EmptyAlgorithmException("Alg is either completely empty at initialisation, or just missing entirely.")

    if isinstance(s, str) is False:
        raise TypeError("Input must be a string.")

    if s.isdigit() or s.replace('.', '').replace('+', '').replace('+', '').isdigit():
        raise ValueError("Input appears to be an integer or a numeric value. Silly.")

    # Check for unmatched brackets.
    _detect_unclosed_brackets(s, Notation.COMM_CONJ_OB, Notation.COMM_CONJ_CB)
    _detect_unclosed_brackets(s, Notation.EXPRESSION_OB, Notation.EXPRESSION_CB)