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

    subparts = sorted(list(parse_brackets(alg)))
    print(subparts)

    while len(subparts) > 0:
        this_subpart = subparts.pop()[1]
        ab = construct_ab(this_subpart)
        if Notation.MULTIPLIER in ab:
            ab = multiplier(ab)
        alg = alg.replace("[" + this_subpart + "]", ab)  # this won't catch a block with more than one nested block inside it.
        print(alg)


    """
    While number of strings != 1:
        1. For the lowest levels:
            if commutator and conjugate:
                special edge case
            if commutator:
                expand A B A' B'
            else if conjugate:
                expand A B A'
            else
                nothing
        2. Replace parent levels string patterns with expanded variants.
        3. Remove children.

    """

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

    comm = (constructor(A, B, 0) if sep == Notation.COMMUTATOR else constructor(A, B, 1))
    return ''.join(comm)


if __name__ == "__main__":



    r = Regex()

    alg_list = [
        #"[U : R U R', D]",
        #"[R,U] R' F R2 U' [R': U'] U R' F'", # t-perm
        "[[M', U],[R D' R' D, F2]]"  # commutator
        #"[U R U': M2][U' R' U: M2]", # M2 method
        #"RUR'U'" # nothing required.
        ]

    for alg in alg_list:

        algo = expand(alg)

        print("Alg raw: {0}".format(algo.raw))
        print("Alg inverse: {0}".format(algo.invert()))
        print("Alg SiGN: {0}".format(algo.to_SiGN()))






