import unittest

from cube.cubes import Cube


class TestCubieMappings(unittest.TestCase):
    def setUp(self):
        self.c = Cube(3)

    def test_edges_no_illegal_pairs(self):
        """
        When edge mappings are generated, then there should be no sticker pairings where the two stickers are opposites.
        """
        illegal_pairs = [(0, 1), (2, 3), (4, 5)]
        distinct_pairs = set(
            [tuple(sorted(i)) for i in list(self.c.edge_mappings.values())]
        )
        for ip in illegal_pairs:
            self.assertNotIn(ip, distinct_pairs)

    def test_edges_no_duplicates(self):
        """
        When edge mappings are generated, then there should be no duplicated tuples.
        """
        distinct_pairs = list(self.c.edge_mappings.values())
        self.assertEqual(len(distinct_pairs), len(set(distinct_pairs)))

    def test_corners_no_illegal_combinations(self):
        """
        When corner mappings are generated, then there should be no sticker triads with two opposite coloured stickers.
        For example, UP face colours and DOWN face colours can't ever be on the same corner cubie.
        """
        illegal_pairs = [(0, 1), (2, 3), (4, 5)]
        distinct_triads = list(self.c.corner_mappings.values())
        for dt in distinct_triads:
            for ip in illegal_pairs:
                self.assertFalse(ip[0] in dt and ip[1] in dt)

    def test_corners_no_duplicates(self):
        """
        When corner mappings are generated, then there should be no duplicated tuples.
        """
        distinct_pairs = list(self.c.corner_mappings.values())
        self.assertEqual(len(distinct_pairs), len(set(distinct_pairs)))


if __name__ == "__main__":
    unittest.main()
