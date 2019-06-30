import unittest

import parse as p
import cube as c


class TestModuleIntegration(unittest.TestCase):

    def setUp(self):
        self.cube = c.Cube(3)
        self.solved = c.Cube(3)

    def test_t_perm(self):
        """
        Given that I can import both the parse and cube packages...
        And I can initialise both an Algorithm object and a Cube object with a T-perm as an input...
        When I input the parsed output from Algorithm to the Cube object...
        Then the state in memory will match that of a T-perm.

        Given that I can initialise both an Algorithm object and a Cube object with a T-perm...
        When I input the inverted T-perm output from Algorithm to the Cube object...
        Then the cube will return to the solved state.
        """
        t_perm = "[R,U] R' (F R2 U' [R': U'] U) R' F'"
        expected_r_face = [[4, 4, 3], [4, 4, 5], [4, 4, 2]]

        t_alg = p.Algorithm(t_perm)
        self.cube.apply(t_alg.alg())

        self.assertListEqual(self.cube.stickers[0:2].tolist(), self.solved.stickers[0:2].tolist())
        self.assertListEqual(self.cube.stickers[4].tolist(), expected_r_face)

        self.cube.apply(t_alg.invert())
        self.assertListEqual(self.cube.stickers.tolist(), self.solved.stickers.tolist())


if __name__ == "__main__":
    unittest.main()
