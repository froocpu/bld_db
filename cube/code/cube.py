from .base_cube import BaseCube


class Cube(BaseCube):
    def __init__(self, nxnxn=3, white_plastic=False):
        super(Cube, self).__init__(N=nxnxn, white_plastic=white_plastic)
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

        self.edge_mappings = {**good_edge_mappings, **bad_edge_mappings}

        print(self.edge_mappings)












