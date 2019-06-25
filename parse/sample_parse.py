import logging

from parse.domain import *

log = logging.getLogger("parse logger")
logging.basicConfig(format=logging.INFO)

if __name__ == "__main__":

    alg_list = [

        "[R,U] R' F R2 U' [R': U'] U R' F'", # t-perm
        "[[M', U],[R D' R' D, F2]]",  # commutator
        "[U R U': M2][U' R' U: M2]",  # M2 method
        "[L: (U M' U M)*2]",  # multiplier
        "RUR'U'", # nothing required.
        "[U : R U R', D]", # cleaner
        "U : R U R', D",  # even cleaner
        "(M' U M U)*2",  # just a multiplier
        "M' U' (M' D')*2 U M'",  # in the middle of a subpart
        "M U' (M U) M U",  # nested
        "[S, R2]",  # throw in some S's
        "[U R': [E, R2]]",  # test Es
        "U"  # one move
        ]

    for alg in alg_list:

        algo = Algorithm(alg)

        print("Alg raw: {0}".format(algo.raw))
        print("Alg moves: {0}".format([m.move for m in algo.moves]))
        print("Alg inverse: {0}".format(algo.invert()))
        print("Alg SiGN: {0}".format(algo.convert_sign()))






