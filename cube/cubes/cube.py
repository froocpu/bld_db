from .base_cube import BaseCube
from parse import Notation

"""
    Print view:

    UDFBRL

    U: x' z
    D: x z
    F: z
    B: x2 z'
    R: x y
    L: x' y'
"""


class Cube(BaseCube):
    def __init__(self, nxnxn=3, white_plastic=False, debug=False):
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
        # TODO: these currently produce a hard-coded object with solved cube mappings. Needs to be abstract.
        # Generate edge mappings.
        good_edge_mappings = {
            "UB": (self.stickers[0][1][2], self.stickers[3][1][2]),
            "UR": (self.stickers[0][2][1], self.stickers[4][1][2]),
            "UF": (self.stickers[0][1][0], self.stickers[2][1][2]),
            "UL": (self.stickers[0][0][1], self.stickers[5][1][2]),
            "DF": (self.stickers[1][1][2], self.stickers[2][1][0]),
            "DR": (self.stickers[1][2][1], self.stickers[4][1][0]),
            "DB": (self.stickers[1][1][0], self.stickers[3][1][0]),
            "DL": (self.stickers[1][0][1], self.stickers[5][0][1]),
            "FL": (self.stickers[2][0][1], self.stickers[5][2][0]),
            "FR": (self.stickers[2][2][1], self.stickers[4][0][1]),
            "BL": (self.stickers[3][2][1], self.stickers[5][0][1]),
            "BR": (self.stickers[3][0][1], self.stickers[4][2][1])
        }

        bad_edge_mappings = {}

        for k in good_edge_mappings:
            new_tuple = (good_edge_mappings[k][1], good_edge_mappings[k][0])
            bad_edge_mappings.update({k[::-1]: new_tuple})

        # Generate corner sticker mappings.
        good_corner_mappings = {
            "ULF": (self.stickers[0][0][0], self.stickers[5][2][2], self.stickers[2][0][2]),
            "UFR": (self.stickers[0][2][0], self.stickers[2][2][2], self.stickers[4][0][2]),
            "URB": (self.stickers[0][2][2], self.stickers[4][2][2], self.stickers[3][0][2]),
            "ULB": (self.stickers[0][0][2], self.stickers[5][0][2], self.stickers[3][2][2]),
            "DLF": (self.stickers[1][0][2], self.stickers[5][2][0], self.stickers[2][0][0]),
            "DFR": (self.stickers[1][2][2], self.stickers[2][2][0], self.stickers[4][0][0]),
            "DRB": (self.stickers[1][2][0], self.stickers[4][2][0], self.stickers[3][0][0]),
            "DLB": (self.stickers[1][0][0], self.stickers[5][0][0], self.stickers[3][2][0])
        }

        # Two clockwise rotations == one counter-clockwise rotation.
        bad_corner_mappings_cw = corner_mapping_rotation_cw(mappings=good_corner_mappings)
        bad_corner_mappings_ccw = corner_mapping_rotation_cw(mappings=bad_corner_mappings_cw)

        # Create final mapping dicts.
        self.edge_mappings = {**good_edge_mappings, **bad_edge_mappings}
        self.corner_mappings = {**good_corner_mappings, **bad_corner_mappings_cw, **bad_corner_mappings_ccw}

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
                m = m.replace(Notation.WIDE)
                for l in range(2):
                    self.base_move(m, l, direction)
            elif m in Notation.WIDE_BLOCKS:
                # Assumes wide turns are written as lowercase.
                face = m.upper()
                for l in range(2):
                    self.base_move(face, l, direction)
            else:
                print("No move required for '{}'.".format(m))
        if self.debug:
            print("Performed move() for {}".format(orig))







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







