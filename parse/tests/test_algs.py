import unittest

from parse.algorithm.config import Validation
from parse.algorithm.algorithm import Algorithm
from parse.exceptions.validation import AmbiguousStatementException, EmptyAlgorithmException, BadMultiplierException, \
    UnclosedBracketsException


class TestAlgorithm(unittest.TestCase):

    def test_vanilla_success(self):
        """
        When simple algorithms are passed as inputs...
        Then the Algorithm class should initialise with no errors...
        And the output algorithm should match the expected alg.
        """
        v1 = Algorithm("RUR'U'")
        v2 = Algorithm("U")

        self.assertListEqual(v1.alg(), ["R", "U", "R'", "U'"])
        self.assertListEqual(v1.invert(), ["U", "R", "U'", "R'"])
        self.assertListEqual(v2.alg(), ["U"])
        self.assertListEqual(v2.invert(), ["U'"])

    def test_vanilla_failed(self):
        """
        When input is None or empty...
        Then the Algorithm class should raise an EmptyAlgorithmException.
        """
        with self.assertRaises(EmptyAlgorithmException):
            Algorithm("")
        with self.assertRaises(EmptyAlgorithmException):
            Algorithm(None)

    def test_illegal_characters_success(self):
        """
        When small typos are present, or illegal characters are passed...
        Then the Algorithm class should initialise with no errors...
        And the output algorithm should match the expected alg.

        Removing illegal characters should not interfere with the intended meaning.
        """
        ic1 = Algorithm("[U: [M', U2]]h")
        ic2 = Algorithm("[U: [pooL, U2]]")

        self.assertListEqual(ic1.alg(), ["U", "M'", "U2", "M", "U2", "U'"])
        self.assertListEqual(ic2.alg(), ["U", "L", "U2", "L'", "U2", "U'"])

    def test_commutator_success(self):
        """
        When commutator notation is provided...
        Then the Algorithm class should initialise with no errors...
        And the output algorithm should match the expected alg.
        """
        comm1 = Algorithm("[S, R2]")
        comm2_nested = Algorithm("[[M', U],[M, D]]")
        comm2_nested_expected = ["M'", "U", "M", "U'", "M", "D", "M'", "D'", "U", "M'", "U'", "M", "D", "M", "D'", "M'"]

        self.assertListEqual(comm1.alg(), ["S", "R2", "S'", "R2"])
        self.assertEqual(comm2_nested.alg(), comm2_nested_expected)

    def test_commutator_failed(self):
        """
        When commutator input is not standard, or ambiguous...
        Then the Algorithm class should raise an AmbiguousStatementException.

        When the commutator notation provided is missing important data...
        Then the Algorithm class should raise an EmptyAlgorithmException.
        """
        with self.assertRaises(AmbiguousStatementException):
            Algorithm("[S, R2, S]")
        with self.assertRaises(AmbiguousStatementException):
            Algorithm("[S, [R2, S, U,, U]]")
        with self.assertRaises(AmbiguousStatementException):
            Algorithm("[S,,U]")
        with self.assertRaises(EmptyAlgorithmException):
            Algorithm(",S")

    def test_conjugate_success(self):
        """
        When conjugate notation is provided...
        Then the Algorithm class should initialise with no errors...
        And the output algorithm should match the expected alg.
        """
        conj1 = Algorithm("[S: R2]")
        conj2_nested = Algorithm("[U: [M: D]]")
        conj2_nested_expected = ["U", "M", "D", "M'", "U'"]

        self.assertListEqual(conj1.alg(), ["S", "R2", "S'"])
        self.assertEqual(conj2_nested.alg(), conj2_nested_expected)

    def test_conjugate_failed(self):
        """
        When conjugated input is not standard, or ambiguous...
        Then the Algorithm class should raise an AmbiguousStatementException.

        When the conjugated notation provided is missing important data...
        Then the Algorithm class should raise an EmptyAlgorithmException.
        """
        with self.assertRaises(AmbiguousStatementException):
            Algorithm("[S: R2: S]")
        with self.assertRaises(AmbiguousStatementException):
            Algorithm("[S: [R2: S: U]]")
        with self.assertRaises(AmbiguousStatementException):
            Algorithm("[S:::U]")
        with self.assertRaises(EmptyAlgorithmException):
            Algorithm("S:")

    def test_combined_success(self):
        """
        When both conjugate and commutator notation is provided in the same alg...
        Then the Algorithm class should initialise with no errors...
        And the output algorithm should match the expected alg.
        """
        c1 = Algorithm("[U R': [E, R2]]")
        c2_single_set = Algorithm("[U : R U R', D]")
        c2_no_brackets = Algorithm("U : R U R', D")

        c1_expected = ["U", "R'", "E", "R2", "E'", "R2", "R", "U'"]
        c2_expected = ["U", "R", "U", "R'", "D", "R", "U'", "R'", "D'", "U'"]

        self.assertListEqual(c1.alg(), c1_expected)
        self.assertEqual(c2_single_set.alg(), c2_expected)
        self.assertEqual(c2_no_brackets.alg(), c2_expected)

    def test_combined_failed(self):
        """
        When combined input is not standard, or ambiguous...
        Then the Algorithm class should raise an AmbiguousStatementException.

        When the combined notation provided is missing important data...
        Then the Algorithm class should raise an EmptyAlgorithmException.
        """
        with self.assertRaises(AmbiguousStatementException):
            Algorithm("[U R': [E, R2] : U]")
        with self.assertRaises(AmbiguousStatementException):
            Algorithm("[U : R U R', D, E]")
        with self.assertRaises(EmptyAlgorithmException):
            Algorithm("[U R': [E,]]")
        with self.assertRaises(EmptyAlgorithmException):
            Algorithm("[: [E,]]")
        with self.assertRaises(EmptyAlgorithmException):
            Algorithm("[: [,]]")

    def test_M2_success(self):
        """
        When M2 method notation is provided...
        Then the Algorithm class should initialise with no errors...
        And the output algorithm should match the expected alg.
        """
        m2 = Algorithm("[U R U': M2][U' R' U: M2]")
        m2_expected = ["U", "R", "U'", "M2", "U", "R'", "U'", "U'", "R'", "U", "M2", "U'", "R", "U"]

        self.assertListEqual(m2.alg(), m2_expected)

    def test_tperm_success(self):
        """
        When variations of the T-perm algorithm is provided...
        Then the Algorithm class should initialise with no errors...
        And the output algorithm should match the expected alg....
        And the inverted algorithm should match the expected inverted alg.
        """
        t = Algorithm("R U R' U' R' F R2 U' R' U' R U R' F'")
        t_shorthand = Algorithm("[R,U] R' F R2 U' [R': U'] U R' F'")
        t_complex = Algorithm("[R,U] (R' F R2) U' [R': U'] U R' F'")

        t_expected = ["R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'", "R", "U", "R'", "F'"]
        t_expected_inverse = ["F", "R", "U'", "R'", "U", "R", "U", "R2", "F'", "R", "U", "R", "U'", "R'"]

        self.assertListEqual(t.alg(), t_expected)
        self.assertListEqual(t_shorthand.alg(), t_expected)
        self.assertListEqual(t_complex.alg(), t_expected)

        self.assertListEqual(t.invert(), t_expected_inverse)
        self.assertListEqual(t_shorthand.invert(), t_expected_inverse)
        self.assertListEqual(t_complex.invert(), t_expected_inverse)

    def test_multiplier_star_success(self):
        """
        When multiplier notation is provided with a multiplier symbol...
        Then the Algorithm class should initialise with no errors...
        And the output algorithm should match the expected alg.
        """
        test_int = 2

        mult1 = Algorithm("(M' U M U)*{}".format(test_int))  # simple multiplier alg
        mult2 = Algorithm("M' U' (M' D')*{} U M'".format(test_int))  # multiplier in middle of normal alg
        mult3 = Algorithm("[L: (U M' U M)*{}]".format(test_int))  # nested inside conjugate
        mult4 = Algorithm("(M' U M U)*1")  # one iteration
        mult5 = Algorithm("(M' U)*4")  # four iterations
        mult6 = Algorithm("U (M' U)*0")  # zero iterations is valid.

        self.assertListEqual(mult1.alg(), ["M'", "U", "M", "U"] * test_int)
        self.assertListEqual(mult2.alg(), ["M'", "U'"] + ["M'", "D'"] * test_int + ["U", "M'"])
        self.assertListEqual(mult3.alg(), ["L"] + ["U", "M'", "U", "M"] * test_int + ["L'"])
        self.assertListEqual(mult4.alg(), ["M'", "U", "M", "U"])
        self.assertListEqual(mult5.alg(), ["M'", "U"] * 4)
        self.assertListEqual(mult6.alg(), ["U"])

    def test_multiplier_no_star_success(self):
        """
        When multiplier notation is provided without a multipler symbol...
        Then the Algorithm class should initialise with no errors...
        And the output algorithm should match the expected alg.
        """
        test_int = 2

        mult1 = Algorithm("(M' U M U){}".format(test_int))  # simple multiplier alg
        mult2 = Algorithm("M' U' (M' D'){} U M'".format(test_int))  # multiplier in middle of normal alg
        mult3 = Algorithm("[L: (U M' U M){}]".format(test_int))  # nested inside conjugate
        mult4 = Algorithm("(M' U M U)1")  # one iteration
        mult5 = Algorithm("(M' U) 4")  # four iterations
        mult6 = Algorithm("U (M' U)0")  # zero iterations is valid.

        self.assertListEqual(mult1.alg(), ["M'", "U", "M", "U"] * test_int)
        self.assertListEqual(mult2.alg(), ["M'", "U'"] + ["M'", "D'"] * test_int + ["U", "M'"])
        self.assertListEqual(mult3.alg(), ["L"] + ["U", "M'", "U", "M"] * test_int + ["L'"])
        self.assertListEqual(mult4.alg(), ["M'", "U", "M", "U"])
        self.assertListEqual(mult5.alg(), ["M'", "U"] * 4)
        self.assertListEqual(mult6.alg(), ["U"])

    def test_multiplier_failed(self):
        """
        When expanded multiplier input is too long...
        Or expanded multipler output is provided with a nonsense value...
        Then the Algorithm class should raise a BadMultiplierException.

        When the multiplier input is missing information...
        Or multiplier input contains a non-integer...
        Then the Algorithm class should raise an EmptyAlgorithmException.
        """
        negative_n = Validation.MULTIPLIER_MIN_REPITITIONS - 100
        too_large_n = Validation.MULTIPLIER_MAX_REPITITIONS * 100

        with self.assertRaises(BadMultiplierException):
            Algorithm("(M' U M U)*{}".format(negative_n))
        with self.assertRaises(BadMultiplierException):
            Algorithm("(M' U M U)*{}".format(too_large_n))
        with self.assertRaises(EmptyAlgorithmException):
            Algorithm("(M' U M U)*{}".format(0))
        with self.assertRaises(BadMultiplierException):
            Algorithm("(M' U M U)*{}".format("a beer"))
        with self.assertRaises(BadMultiplierException):
            Algorithm("(M' U M U)*{}".format(None))

    def test_brackets_success(self):
        """
        When brackets are provided...
        Then the Algorithm class should initialise with no errors...
        And the output algorithm should match the expected alg.
        """
        br = Algorithm("M U' (M U) M U")
        self.assertListEqual(br.alg(), ["M", "U'", "M", "U", "M", "U"])

    def test_brackets_failed(self):
        """
         When input contains unclosed brackets...
         Then the Algorithm class should raise an UnclosedBracketsException.
         """
        with self.assertRaises(UnclosedBracketsException):
            Algorithm("M U' (M U M U")
        with self.assertRaises(UnclosedBracketsException):
            Algorithm("(M U' M U M U))")
        with self.assertRaises(UnclosedBracketsException):
            Algorithm("M U' [M, U M U")
        with self.assertRaises(UnclosedBracketsException):
            Algorithm("[S, R2]]")


if __name__ == "__main__":
    unittest.main()