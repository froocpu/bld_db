from cube.cubes import Cube
from cube.utils import niklas


if __name__ == "__main__":

    c = Cube(3, white_plastic=False)

    #niklas(c)
    c.move("M")
    print(c.stickers[:, 1, :])