from cube.cubes import Cube
from cube.utils import niklas


if __name__ == "__main__":

    c = Cube(3, white_plastic=False)

    niklas(c)
    print(c.stickers)