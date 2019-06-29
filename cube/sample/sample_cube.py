from cube.code import Cube


def commutator(cube):
    """
    Execute a commutator.
    """
    cube.base_move("R", 0, -1)
    cube.base_move("D", 0, -1)
    cube.base_move("R", 0, 1)
    cube.base_move("U", 0, 2)
    cube.base_move("R", 0, -1)
    cube.base_move("D", 0, 1)
    cube.base_move("R", 0, 1)
    cube.base_move("U", 0, 2)
    cube.render("test.png")


def MU2MU2(cube):
    """
    Execute a commutator.
    """
    cube.base_move("R", 0, -1)
    cube.base_move("L", 0, 1)
    cube.base_move("F", 0, 2)
    cube.base_move("R", 0, 1)
    cube.base_move("L", 0, -1)
    cube.base_move("U", 0, 2)

    cube.render("test.png")


def DU2DU2(cube):
    """
    Execute a commutator.
    """
    cube.base_move("R", 0, 1)
    cube.base_move("L", 0, -1)
    cube.base_move("D", 0, 2)
    cube.base_move("R", 0, -1)
    cube.base_move("L", 0, 1)
    cube.base_move("B", 0, 2)

    cube.render("test.png")


def EU2EU2(cube):
    """
    Execute a commutator.
    """
    cube.base_move("U", 0, -1)
    cube.base_move("D", 0, 1)
    cube.base_move("R", 0, 2)
    cube.base_move("D", 0, -1)
    cube.base_move("U", 0, 1)
    cube.base_move("F", 0, 2)

    cube.render("test.png")


def niklas(cube):
    """
    Niklas comm.
    """
    cube.base_move("U", 0, 1)
    cube.base_move("R", 0, 1)
    cube.base_move("U", 0, -1)
    cube.base_move("L", 0, -1)
    cube.base_move("U", 0, 1)
    cube.base_move("R", 0, -1)
    cube.base_move("U", 0, -1)
    cube.base_move("L", 0, 1)


def MU2MU2_updated(cube):
    """
    Niklas comm.
    """
    cube.move("M'")
    cube.move("U2")
    cube.move("M")
    cube.move("U2")


if __name__ == "__main__":
    """
    Functional testing.
    """
    c = Cube(3, white_plastic=False)

    # MU2MU2(c)
    # MU2MU2(c)
    # DU2DU2(c)
    # DU2DU2(c)
    # EU2EU2(c)
    # EU2EU2(c)
    # niklas(c)
    # niklas(c)
    MU2MU2_updated(c)
    c.move("y")
    print(c.stickers)