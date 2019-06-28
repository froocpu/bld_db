from .base_cube import BaseCube


class Cube(BaseCube):
    def __init__(self, nxnxn=3, white_plastic=False):
        super(Cube, self).__init__(N=nxnxn, white_plastic=white_plastic)

    # TODO: add wrapper methods for easier use.




