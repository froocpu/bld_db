from cube.code import Cube


def commutator(cube):
    """
    Execute a commutator.
    """
    cube.move("R", 0, -1)
    cube.move("D", 0, -1)
    cube.move("R", 0, 1)
    cube.move("U", 0, 2)
    cube.move("R", 0, -1)
    cube.move("D", 0, 1)
    cube.move("R", 0, 1)
    cube.move("U", 0, 2)
    cube.render("test.png")


def MU2MU2(cube):
    """
    Execute a commutator.
    """
    cube.move("R", 0, -1)
    cube.move("L", 0, 1)
    cube.move("F", 0, 2)
    cube.move("R", 0, 1)
    cube.move("L", 0, -1)
    cube.move("U", 0, 2)

    cube.render("test.png")


def DU2DU2(cube):
    """
    Execute a commutator.
    """
    cube.move("R", 0, 1)
    cube.move("L", 0, -1)
    cube.move("D", 0, 2)
    cube.move("R", 0, -1)
    cube.move("L", 0, 1)
    cube.move("B", 0, 2)

    cube.render("test.png")


def EU2EU2(cube):
    """
    Execute a commutator.
    """
    cube.move("U", 0, -1)
    cube.move("D", 0, 1)
    cube.move("R", 0, 2)
    cube.move("D", 0, -1)
    cube.move("U", 0, 1)
    cube.move("F", 0, 2)

    cube.render("test.png")


if __name__ == "__main__":
    """
    Functional testing.
    """
    c = Cube(3, white_plastic=False)

    # MU2MU2(c)
    # MU2MU2(c)
    # DU2DU2(c)
    # DU2DU2(c)
    EU2EU2(c)
    EU2EU2(c)
    print(c.stickers)
    c.render("test.png")

    print(c.stickers[0][1][2]) # UF - 1 = down sticker
    print(c.stickers[2][1][0]) # FU - 2 = front sticker = DF.

    print(c.stickers[0][1][0]) # UB
    print(c.stickers[3][1][2]) # BU

    print(c.stickers[1][1][2]) # DF
    print(c.stickers[2][1][2]) # FU