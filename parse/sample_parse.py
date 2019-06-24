import logging

from parse.domain import *
from parse.exceptions import *
from parse.utils import *

log = logging.getLogger("parse logger")
logging.basicConfig(format=logging.INFO)


def expand(s):
    """
    Until I know where to put this, this will take a raw string, parse it and create an "Algorithm" object.
    :param raw:
    :return: Algorithm
    """
    alg = clean_alg(s)
    print(alg)

    # Process smaller, nested brackets.
    while r.match_sequence(alg) is not None:

        this_match = r.match_sequence(alg)
        this_str = this_match.replace("[", "").replace("]", "")
        comm_str = construct_ab(this_str)
        alg = alg.replace(this_match, comm_str)

    # Process outer conjugates/commutators.
    if Notation.COMMUTATOR not in alg and Notation.CONJUGATE not in alg:
        return Algorithm(alg)

    if Notation.COMMUTATOR in alg and Notation.CONJUGATE in alg:
        raise AmbiguousStatementException("Syntax contains both commutator and conjugate notation with no brackets.")

    alg = construct_ab(alg)
    return Algorithm(alg)


def construct_ab(s):
    """
    Until I know where to put this, this will take a raw string and split it into A and B components.
    :param s: raw algorithm.
    :return: str - expanded algorithm
    """
    if Notation.COMMUTATOR in s:
        sep = Notation.COMMUTATOR
    else:
        sep = Notation.CONJUGATE

    A, B = split_ab(s, sep)
    A = [Move(m) for m in split_sequence(A)]
    B = [Move(m) for m in split_sequence(B)]

    comm = (construct_commutator(A, B) if sep == Notation.COMMUTATOR else construct_conjugate(A, B))
    return ''.join(comm)


if __name__ == "__main__":

    r = Regex()

    alg_list = [
        #"[U : R U R', D]",
        "[R,U] R' F R2 U' [R': U'] U R' F'", # t-perm
        "[D: [R D' R' D, F2]]", # commutator
        # TODO: breaks here
        "[U R U': M2][U' R' U: M2]", # M2 method
        "RUR'U'" # nothing required.
        ]

    for alg in alg_list:

        algo = expand(alg)

        print("Alg raw: {0}".format(algo.raw))
        print("Alg inverse: {0}".format(algo.invert()))
        print("Alg SiGN: {0}".format(algo.to_SiGN()))






