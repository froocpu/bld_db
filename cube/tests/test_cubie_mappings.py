import unittest

from cube.code import Cube


class TestCubieMappings(unittest.TestCase):

    def setUp(self):
        self.c = Cube(3)

    def test_edges_no_illegal_pairs(self):
        """
        When the mappings are generated, then there should be no sticker pairings where the two stickers are opposites.
        """
        illegal_pairs = [(0, 1), (2, 3), (4, 5)]
        distinct_pairs = set([tuple(sorted(i)) for i in list(self.c.edge_mappings.values())])
        print(distinct_pairs)
        for ip in illegal_pairs:
            self.assertNotIn(ip, distinct_pairs)

    def test_edges_no_duplicates(self):
        """
        When mappings are generated, then there should be no duplicated tuples.
        """
        distinct_pairs = list(self.c.edge_mappings.values())
        self.assertEqual(len(distinct_pairs), len(set(distinct_pairs)))


if __name__ == "__main__":
    unittest.main()
