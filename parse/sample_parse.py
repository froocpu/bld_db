import logging

from parse.domain import *

log = logging.getLogger("parse logger")
logging.basicConfig(format=logging.INFO)

if __name__ == "__main__":

    alg_list = [

        "[R,U] R' F R2 U' [R': U'] U R' F'"
        ]

    for alg in alg_list:

        algo = Algorithm(alg)

        print("Alg raw: {0}".format(algo.raw))
        print("Alg moves: {0}".format([m.move for m in algo.moves]))
        print("Alg inverse: {0}".format(algo.invert()))
        print("Alg SiGN: {0}".format(algo.convert_sign()))






