import unittest

from parse.domain import Algorithm


class TestAlgorithm(unittest.TestCase):

    def test_vanilla(self):

        v1 = Algorithm("RUR'U'")
        v2 = Algorithm("U")
        v3 = Algorithm("\t  D D \t D        D\n")  # silly whitespace

        self.assertListEqual(v1.alg(), ["R", "U", "R'", "U'"])
        self.assertListEqual(v1.invert(), ["U", "R", "U'", "R'"])
        self.assertListEqual(v2.alg(), ["U"])
        self.assertListEqual(v2.invert(), ["U'"])
        self.assertListEqual(v3.alg(), ["D"] * 4)
        self.assertListEqual(v3.invert(), ["D'"] * 4)

    def test_commutator(self):

        comm1 = Algorithm("[S, R2]")
        comm2_nested = Algorithm("[[M', U],[M, D]]")

        comm2_nested_expected = ["M'", "U", "M", "U'", "M", "D", "M'", "D'", "U", "M'", "U'", "M", "D", "M", "D'", "M'"]

        self.assertListEqual(comm1.alg(), ["S", "R2", "S'", "R2"])
        self.assertEqual(comm2_nested.alg(), comm2_nested_expected)

    def test_conjugate(self):

        conj1 = Algorithm("[S: R2]")
        conj2_nested = Algorithm("[U: [M: D]]")

        conj2_nested_expected = ["U", "M", "D", "M'", "U'"]

        self.assertListEqual(conj1.alg(), ["S", "R2", "S'"])
        self.assertEqual(conj2_nested.alg(), conj2_nested_expected)

    def test_combined(self):

        c1 = Algorithm("[U R': [E, R2]]")
        c2_single_set = Algorithm("[U : R U R', D]")
        c2_no_brackets = Algorithm("U : R U R', D")

        c1_expected = ["U", "R'", "E", "R2", "E'", "R2'", "R", "U'"]
        c2_expected = ["U", "R", "U", "R'", "D", "R", "U'", "R'", "D'", "U'"]

        self.assertListEqual(c1.alg(), c1_expected)
        self.assertEqual(c2_single_set.alg(), c2_expected)
        self.assertEqual(c2_no_brackets.alg(), c2_expected)

    def test_M2(self):

        m2 = Algorithm("[U R U': M2][U' R' U: M2]")
        m2_expected = ["U", "R", "U'", "M2", "U", "R'", "U'", "U'", "R'", "U", "M2", "U'", "R", "U"]

        self.assertListEqual(m2.alg(), m2_expected)

    def test_tperm(self):

        t = Algorithm("R U R' U' R' F R2 U' R' U' R U R' F'")
        t_shorthand = Algorithm("[R,U] R' F R2 U' [R': U'] U R' F'")
        t_complex = Algorithm("[R,U] (R' F R2) U' [R': U'] U R' F'")

        t_expected = ["R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'", "R", "U", "R'", "F'"]
        t_expected_inverse = ["F", "R", "U'", "R'", "U", "R", "U", "R2'", "F'", "R", "U", "R", "U'", "R'"]

        self.assertListEqual(t.alg(), t_expected)
        self.assertListEqual(t_shorthand.alg(), t_expected)
        self.assertListEqual(t.invert(), t_expected_inverse)

    def test_multiplier(self):

        test_int = 2

        mult1 = Algorithm("(M' U M U)*{}".format(test_int))  # simple multiplier alg
        mult2 = Algorithm("M' U' (M' D')*{} U M'".format(test_int))  # multiplier in middle of normal alg
        mult3 = Algorithm("[L: (U M' U M)*{}]".format(test_int))  # nested inside conjugate
        mult4 = Algorithm("(M' U M U)*1")  # one iteration
        mult5 = Algorithm("(M' U)*4")  # four iterations

        self.assertListEqual(mult1.alg(), ["M'", "U", "M", "U"] * test_int)
        self.assertListEqual(mult2.alg(), ["M'", "U'"] + ["M'", "D'"] * test_int + ["U", "M'"])
        self.assertListEqual(mult3.alg(), ["L"] + ["U", "M'", "U", "M"] * test_int + ["L'"])
        self.assertListEqual(mult4.alg(), ["M'", "U", "M", "U"])
        self.assertListEqual(mult5.alg(), ["M'", "U"] * 4)

    def test_brackets(self):

        br = Algorithm("M U' (M U) M U")

        self.assertListEqual(br.alg(), ["M", "U'", "M", "U", "M", "U"])


