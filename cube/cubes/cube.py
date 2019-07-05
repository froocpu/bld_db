from .base_cube import BaseCube
from parse import Notation
from ..utils.strings import rotate_sticker


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
        self.unsolved_edge_count = 0
        self.unsolved_corner_count = 0
        self.unsolved_corners = []
        self.unsolved_edges = []
        self.solved_state_corners, self.solved_state_edges = _generate_good_mappings(self.stickers)

        self.reverse_dict = {}
        for v in self.facedict:
            self.reverse_dict.update({self.facedict[v]: v})

        # Generate mappings.
        good_corner_mappings, good_edge_mappings = self.solved_state_corners, self.solved_state_edges

        bad_edge_mappings = flip_edge_mappings(good_edge_mappings)

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
        self.update()

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

    def update(self):
        """
        Updates the current mapping states and unsolved piece counts.
        :return: None
        """
        # Refresh the existing lists.
        corner_mappings, edge_mappings = _generate_good_mappings(self.stickers)

        for c in corner_mappings:
            if corner_mappings[c] != self.solved_state_corners[c]:
                self.unsolved_corners.append(c)
        for e in edge_mappings:
            if edge_mappings[e] != self.solved_state_edges[e]:
                self.unsolved_edges.append(e)

        self.unsolved_edge_count = len(self.unsolved_edges)
        self.unsolved_corner_count = len(self.unsolved_corners)

        edge_mappings_inverse = flip_edge_mappings(edge_mappings)

        # Two clockwise rotations == one counter-clockwise rotation.
        corner_mappings_cw = corner_mapping_rotation_cw(mappings=corner_mappings)
        corner_mappings_ccw = corner_mapping_rotation_cw(mappings=corner_mappings_cw)

        self.edge_mappings = {**edge_mappings, **edge_mappings_inverse}
        self.corner_mappings = {**corner_mappings, **corner_mappings_cw, **corner_mappings_ccw}

    def corner_cycle_discovery(self):
        """
        # TODO: make dynamic. edges and corners discovery can be combined.
        """
        all_corner_cycles = []

        for j in self.unsolved_corners:

            if any([j in k for k in all_corner_cycles]) or any([rotate_sticker(j, cw=True) in k for k in all_corner_cycles]) or any([rotate_sticker(j, cw=False) in k for k in all_corner_cycles]):
                continue

            this_cycle = [j]
            end_cycle_piece = [j, rotate_sticker(j, cw=False), rotate_sticker(j, cw=True)]

            while True:
                this_piece = self.corner_mappings[this_cycle[-1]]
                sticker = "".join([self.reverse_dict[this_piece[l]] for l in range(3)])
                if sticker in end_cycle_piece:
                    all_corner_cycles.append(this_cycle)
                    break
                this_cycle.append(sticker)

        return all_corner_cycles

    def edge_cycle_discovery(self):
        """
        Search a cube state for cycles of unsolved pieces.

        Workflow:

            1. Use a reversed copy of self.facedict to use to lookup pieces based on their sticker index.
               For example, when 012345 == UDFBRL then (0, 2, 4) == UFR.
            2. Get to work:
                - If we have already discovered a cycle with this piece inside it, skip it.
                - Get the starting position and create a 'flipped' version to close the cycle when the buffer is flipped.
            3. Keep searching for pieces as long as the cycle is not finished:
                - Get the stickers of the piece in the location of the last piece in the cycle so far.
                - Convert ints to sticker notation and add to the cycle, unless it's the buffer sticker, then finish off the cycle.

        :return: list
        """
        all_edge_cycles = []

        for j in self.unsolved_edges:

            if any([j in k for k in all_edge_cycles]) or any([rotate_sticker(j) in k for k in all_edge_cycles]):
                continue

            this_cycle = [j]
            end_cycle_piece = [j, rotate_sticker(j)]

            while True:
                this_piece = self.edge_mappings[this_cycle[-1]]
                sticker_a, sticker_b = self.reverse_dict[this_piece[0]], self.reverse_dict[this_piece[1]]
                sticker = "".join([sticker_a, sticker_b])
                if sticker in end_cycle_piece:
                    all_edge_cycles.append(this_cycle)
                    break
                this_cycle.append(sticker)

        return all_edge_cycles


def _generate_good_mappings(stickers):
    """
    Internal function. Used to take a snapshot of the cube and calculate metadata on states.
    :param stickers: a set of stickers (m-n array), solved or not.
    :return: dict

    Note: by changing the order of the fields, you can influence the order in which the cycle pieces appear in the cycles objects.
    """
    corners = {
        "UBL": (stickers[0][0][2], stickers[3][2][2], stickers[5][0][2]),
        "URB": (stickers[0][2][2], stickers[4][2][2], stickers[3][0][2]),
        "UFR": (stickers[0][2][0], stickers[2][2][2], stickers[4][0][2]),
        "ULF": (stickers[0][0][0], stickers[5][2][2], stickers[2][0][2]),
        "DFL": (stickers[1][0][2], stickers[2][0][0], stickers[5][2][0]),
        "DRF": (stickers[1][2][2], stickers[4][0][0], stickers[2][2][0]),
        "DBR": (stickers[1][2][0], stickers[3][0][0], stickers[4][2][0]),
        "DLB": (stickers[1][0][0], stickers[5][0][0], stickers[3][2][0])
    }

    edges = {
        "UF": (stickers[0][1][0], stickers[2][1][2]),
        "DF": (stickers[1][1][2], stickers[2][1][0]),
        "UB": (stickers[0][1][2], stickers[3][1][2]),
        "UR": (stickers[0][2][1], stickers[4][1][2]),
        "UL": (stickers[0][0][1], stickers[5][1][2]),
        "DR": (stickers[1][2][1], stickers[4][1][0]),
        "DB": (stickers[1][1][0], stickers[3][1][0]),
        "DL": (stickers[1][0][1], stickers[5][1][0]),
        "FL": (stickers[2][0][1], stickers[5][2][1]),
        "FR": (stickers[2][2][1], stickers[4][0][1]),
        "BL": (stickers[3][2][1], stickers[5][0][1]),
        "BR": (stickers[3][0][1], stickers[4][2][1])
    }

    return corners, edges


def flip_edge_mappings(mappings):
    """
    Perform a flip on an edges mapping object, generating new keys and tuples.
    :param mappings: a dictionary of mappings of human-readable notation to multi-dimensional array indices.
    :type: dict
    :return: dict
    """
    bad_edge_mappings = {}
    for k in mappings:
        new_tuple = (mappings[k][1], mappings[k][0])
        bad_edge_mappings.update({k[::-1]: new_tuple})
    return bad_edge_mappings


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







