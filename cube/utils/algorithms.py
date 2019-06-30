def _helper(cube, alg, cycle=True):
    """
    For each move in alg, apply the move to a cube.
    Perform the algorithm twice to set up the case if it is a commutator, else just perform it once.
    :param cube: a Cube class instance.
    :type: Cube
    :param alg: list of moves
    :type alg: list of str
    :param cycle: if the alg leaves a 3-cycle, then True.
    :type cycle: bool
    """
    seq = alg
    if cycle:
        seq = alg + alg
    for move in seq:
        cube.move(move)


def corner_commutator(cube):
    """
    Execute a corner commutator.
    """
    alg = ["R'", "D'", "R", "U2", "R'", "D", "R", "U2"]
    _helper(cube, alg)


def niklas(cube):
    """
    Niklas commutator.
    """
    alg = ["U", "R", "U'", "L'", "U", "R'", "U'", "L"]
    _helper(cube, alg)


def wide_commutator(cube):
    """
    M2 style commutator.
    """
    alg = ["u", "R", "u'", "M2", "u", "R'", "u'", "M2"]
    _helper(cube, alg)


def t_perm(cube):
    """
    T-perm PLL.
    """
    alg = ['R', 'U', "R'", "U'", "R'", 'F', 'R2', "U'", "R'", "U'", 'R', 'U', "R'", "F'"]
    _helper(cube=cube, alg=alg, cycle=False)
