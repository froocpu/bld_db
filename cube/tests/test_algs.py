import unittest

from cube.cubes import Cube
from cube.utils import wide_commutator, corner_commutator, t_perm, niklas


class TestAlgs(unittest.TestCase):
    def setUp(self):
        self.cube = Cube(3)
        self.solved = Cube(3)

    def test_niklas(self):
        """
        When I apply a Niklas commutator to the cube...
        Then the D face should remain unchanged...
        And the U face should match the expected state.
        """
        niklas(self.cube)
        expected_u_face = [[3, 0, 2], [0, 0, 0], [0, 0, 5]]
        self.assertListEqual(
            self.cube.stickers[1].tolist(), self.solved.stickers[1].tolist()
        )
        self.assertListEqual(self.cube.stickers[0].tolist(), expected_u_face)

    def test_tperm(self):
        """
        When I apply a T-perm to a fresh cube...
        Then I am expecting the U face to match a solved U face...
        And I expect the D face to match a solved D face...
        And I expect the R face to match the list below.

        When I apply a second iteration of the T-perm...
        Then I expect the cube to be solved.
        """
        t_perm(self.cube)
        expected_r_face = [[4, 4, 3], [4, 4, 5], [4, 4, 2]]
        self.assertListEqual(
            self.cube.stickers[0:2].tolist(), self.solved.stickers[0:2].tolist()
        )
        self.assertListEqual(self.cube.stickers[4].tolist(), expected_r_face)

        t_perm(self.cube)
        self.assertListEqual(self.cube.stickers.tolist(), self.solved.stickers.tolist())

    def test_corner_commutator(self):
        """
        When I apply a corner commutator to the cube...
        Then there should be no matching faces...
        And the U face should match the expected state...
        And the R face should match the expected state.
        """
        corner_commutator(self.cube)
        expected_u_face = [[0, 0, 4], [0, 0, 0], [0, 0, 0]]
        expected_r_face = [[0, 4, 5], [4, 4, 4], [4, 4, 4]]

        for i, face in enumerate(self.cube.stickers):
            self.assertFalse((face == self.solved.stickers[i]).all())
        self.assertListEqual(self.cube.stickers[0].tolist(), expected_u_face)
        self.assertListEqual(self.cube.stickers[4].tolist(), expected_r_face)

    def test_wide_commutator(self):
        """
        When I apply a wide block commutator to the cube...
        Then only the left face should match a solved cube...
        And the U face should match the expected state...
        And the D face should match the expected state...
        And the F face should match the expected state.
        """
        wide_commutator(self.cube)
        expected_u_face = [[0, 0, 0], [0, 0, 1], [0, 0, 0]]
        expected_d_face = [[1, 1, 1], [1, 1, 4], [1, 1, 1]]
        expected_f_face = [[2, 2, 2], [3, 2, 2], [2, 2, 2]]

        self.assertListEqual(
            self.cube.stickers[5].tolist(), self.solved.stickers[5].tolist()
        )
        self.assertListEqual(self.cube.stickers[0].tolist(), expected_u_face)
        self.assertListEqual(self.cube.stickers[1].tolist(), expected_d_face)
        self.assertListEqual(self.cube.stickers[2].tolist(), expected_f_face)
