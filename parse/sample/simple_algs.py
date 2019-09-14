import logging

from parse.algorithm import Algorithm

log = logging.getLogger("parse logger")
logging.basicConfig(format=logging.INFO)

if __name__ == "__main__":

    my_tperm = "[R,U] R' F R2 U' [R': U'] U R' F'"
    my_favourite_commutator = "[D: [R2, S']]"
    my_m2_algs = "[U R U' : M2][U' L2 U : M2]"
    my_mu_alg = "(M' U M U)*2"

    t_perm = Algorithm(my_tperm)
    print(t_perm.alg())
    print(t_perm.invert())

    comm = Algorithm(my_favourite_commutator)
    print(comm.alg())
    print(comm.invert())

    m2 = Algorithm(my_m2_algs)
    print(m2.alg())

    mu = Algorithm(my_mu_alg)
    print(mu.alg())
    print(mu.raw)
