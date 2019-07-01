from .base_cube import BaseCube
from parse import Notation


class Cube(BaseCube):
    def __init__(self, nxnxn=3, white_plastic=True, debug=False):
        """
        Initialised in a similar way to the underlying BaseCube class, so inherting the BaseClass will also transfer
        all of the same fields and methods over.
        :param nxnxn: 3 for a standard Rubik's Cube, 4 for a Professor Cube, etc.
        :type nxnxn: int
        :param white_plastic: when True, rendered images use white plastic, else black.
        :type white_plastic: bool
        :param debug: if True, be verbose. Mostly for logging and testing purposes.
        :type debug: bool
        """
        super(Cube, self).__init__(N=nxnxn, white_plastic=white_plastic)
        self.nxnxn = nxnxn
        self.debug = debug
        self.solved_state_corners, self.solved_state_edges = self._generate_good_mappings(self.stickers)
        self.unsolved_edge_count = 0
        self.unsolved_corner_count = 0
        self.unsolved_corners = []
        self.unsolved_edges = []

        # Generate mappings.
        good_corner_mappings, good_edge_mappings = self.solved_state_corners, self.solved_state_edges

        bad_edge_mappings = {}

        for k in good_edge_mappings:
            new_tuple = (good_edge_mappings[k][1], good_edge_mappings[k][0])
            bad_edge_mappings.update({k[::-1]: new_tuple})

        # Two clockwise rotations == one counter-clockwise rotation.
        bad_corner_mappings_cw = corner_mapping_rotation_cw(mappings=good_corner_mappings)
        bad_corner_mappings_ccw = corner_mapping_rotation_cw(mappings=bad_corner_mappings_cw)

        # Create final mapping dicts.
        self.edge_mappings = {**good_edge_mappings, **bad_edge_mappings}
        self.corner_mappings = {**good_corner_mappings, **bad_corner_mappings_cw, **bad_corner_mappings_ccw}

    def apply(self, alg):
        """
        For each move in alg, apply a move to the cube representation.
        Assumes that alg has been properly parsed, sanitised and validated.
        :param alg: list of strings representing cleaned moves.
        :type alg: list of str
        :return: None
        """
        for move in alg:
            self.move(move)
        self.count_unsolved_pieces()

    def move(self, m):
        """
        Wrapper for base_move. Call the inherited base_move and update the stickers field.
        :param m: face/slice/block to turn. Should be a validated and sanitised move string from Algorithm.
        :type m: str
        :return: None
        TODO: adapt for larger cubes
        """
        orig = m
        direction = 1
        if m.endswith(Notation.PRIME):
            direction = -1
            m = m.replace(Notation.PRIME, Notation.EMPTY)
        if m.endswith(Notation.DOUBLE):
            direction = 2
            m = m.replace(Notation.DOUBLE, Notation.EMPTY)

        if self.nxnxn == 3:
            if m in Notation.BLOCKS:
                self.base_move(m, 0, direction)
            elif m in Notation.SLICES:
                # Note: slice convention is weird and counter-intuitive.
                if m == Notation.SLICE_FOLLOWS_D:
                    face = Notation.DOWN_FACE_CHAR
                elif m == Notation.SLICE_FOLLOWS_L:
                    face = Notation.LEFT_FACE_CHAR
                else:
                    face = Notation.FRONT_FACE_CHAR
                self.base_move(face, 1, direction)
            elif m in Notation.ROTATIONS:
                if m == Notation.ROTATION_FOLLOWS_U:
                    face = Notation.UP_FACE_CHAR
                elif m == Notation.ROTATION_FOLLOWS_F:
                    face = Notation.FRONT_FACE_CHAR
                else:
                    face = Notation.RIGHT_FACE_CHAR
                self.turn(face, direction)
            # Two variations of wide turn notation to process.
            elif m.endswith(Notation.WIDE):
                m = m.replace(Notation.WIDE, Notation.EMPTY)
                for l in range(2):
                    self.base_move(m, l, direction)
            elif m in Notation.WIDE_BLOCKS:
                # Assumes wide turns are written as lowercase.
                face = m.upper()
                for l in range(2):
                    self.base_move(face, l, direction)
        if self.debug:
            print("Performed move() for {}".format(orig))

    @staticmethod
    def _generate_good_mappings(stickers):
        """
        Internal function. Used to take a snapshot of the cube and calculate metadata on states.
        :param stickers: a set of stickers (m-n array), solved or not.
        :return: dict
        """
        good_corner_mappings = {
            "ULF": (stickers[0][0][0], stickers[5][2][2], stickers[2][0][2]),
            "UFR": (stickers[0][2][0], stickers[2][2][2], stickers[4][0][2]),
            "URB": (stickers[0][2][2], stickers[4][2][2], stickers[3][0][2]),
            "ULB": (stickers[0][0][2], stickers[5][0][2], stickers[3][2][2]),
            "DLF": (stickers[1][0][2], stickers[5][2][0], stickers[2][0][0]),
            "DFR": (stickers[1][2][2], stickers[2][2][0], stickers[4][0][0]),
            "DRB": (stickers[1][2][0], stickers[4][2][0], stickers[3][0][0]),
            "DLB": (stickers[1][0][0], stickers[5][0][0], stickers[3][2][0])
        }

        good_edge_mappings = {
            "UB": (stickers[0][1][2], stickers[3][1][2]),
            "UR": (stickers[0][2][1], stickers[4][1][2]),
            "UF": (stickers[0][1][0], stickers[2][1][2]),
            "UL": (stickers[0][0][1], stickers[5][1][2]),
            "DF": (stickers[1][1][2], stickers[2][1][0]),
            "DR": (stickers[1][2][1], stickers[4][1][0]),
            "DB": (stickers[1][1][0], stickers[3][1][0]),
            "DL": (stickers[1][0][1], stickers[5][1][0]),
            "FL": (stickers[2][0][1], stickers[5][2][1]),
            "FR": (stickers[2][2][1], stickers[4][0][1]),
            "BL": (stickers[3][2][1], stickers[5][0][1]),
            "BR": (stickers[3][0][1], stickers[4][2][1])
        }

        return good_corner_mappings, good_edge_mappings

    def count_unsolved_pieces(self):
        """
        Compare the current state against the solved state. Count the number of pieces out of place.
        :return: None
        """
        # Refresh the existing lists.
        self.unsolved_edge_count = []
        self.unsolved_corner_count = []

        unsolved_edge_count = 0
        unsolved_corner_count = 0
        current_corner_mappings, current_edge_mappings = self._generate_good_mappings(self.stickers)
        for c in current_corner_mappings:
            if current_corner_mappings[c] != self.solved_state_corners[c]:
                unsolved_corner_count += 1
                self.unsolved_corners.append(c)
        for e in current_edge_mappings:
            if current_edge_mappings[e] != self.solved_state_edges[e]:
                unsolved_edge_count += 1
                self.unsolved_edges.append(e)

        self.unsolved_edge_count = unsolved_edge_count
        self.unsolved_corner_count = unsolved_corner_count


def corner_mapping_rotation_cw(mappings):
    """
    Perform a clockwise rotation on a mappings object, generating new keys and tuples. Required for corners only.
    :param mappings: a dictionary of mappings of human-readable notation to multi-dimensional array indices.
    :type: dict
    :return: dict
    """
    new_dict = {}
    for k in mappings:
        new_key = "".join([k[1], k[2], k[0]])
        new_tuple = (mappings[k][1], mappings[k][2], mappings[k][0])
        new_dict.update({new_key: new_tuple})
    return new_dict







