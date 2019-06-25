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
        # BROKEN #  "U : R U R', D"  # even cleaner

        ]

    for alg in alg_list:

        algo = Algorithm(alg)

        print("Alg raw: {0}".format(algo.raw))
        print("Alg moves: {0}".format([m.move for m in algo.moves]))
        print("Alg inverse: {0}".format(algo.invert()))
        print("Alg SiGN: {0}".format(algo.convert_sign()))






