from .strings import signature, split_note
from numpy import array_equal


def analyze(cube, notes=None):
    """
    Perform cycle discovery on the cube and calculate metadata about the alg.
    :param cube: Cube object with moves applied.
    :type cube: Cube
    :param notes: extracted earlier in the pipeline, this is the accompanying note for a cell.
    :type notes: str
    :return: a dict containing the results

    TODO: process notes object.
    """
    edge_cycles = cube.edge_cycle_discovery()
    corner_cycles = cube.corner_cycle_discovery()

    flipped_edge_count = len([j for j in edge_cycles if len(j) == 1])
    twisted_corner_count = len([j for j in corner_cycles if len(j) == 1])

    parity_calculation = sum([len(targets) - 1 for targets in edge_cycles]) % 2
    parity_flag = (True if parity_calculation == 1 and flipped_edge_count == 0 else False)

    # Determine what kind of 3x3x3 alg this would be.
    if array_equal(cube.stickers[2:, :, 0:2], cube.stickers_solved[2:, :, 0:2]) and array_equal(cube.stickers[1], cube.stickers_solved[1]):
        ll_flag = True
        if array_equal(cube.stickers[0], cube.stickers_solved[0]):
            pll_flag = True
            oll_flag, coll_flag = False, False
            ell_flag = (True if len(corner_cycles) == 0 else False)
        elif array_equal(cube.stickers[0, 1], cube.stickers_solved[0, 1]) and array_equal(cube.stickers[0, 1, :], cube.stickers_solved[0, 1, :]):
            coll_flag, oll_flag = True, True
            pll_flag, ell_flag = False, False
        # if U layer corners are oriented.
        elif len(corner_cycles) == 0:
            coll_flag, pll_flag = False, False
            oll_flag, ell_flag = True, True
        else:
            pll_flag, coll_flag, ell_flag = False, False, False
            oll_flag = True
    else:
        ll_flag, pll_flag, oll_flag, coll_flag, ell_flag = False, False, False, False, False

    bundle = {"edge_cycles": edge_cycles,
              "corner_cycles": corner_cycles,
              "unsolved_edges_count": cube.unsolved_edge_count,
              "unsolved_corners_count": cube.unsolved_corner_count,
              "flipped_edges_count": flipped_edge_count,
              "twisted_corners_count": twisted_corner_count,
              "parity_flag": parity_flag,
              "ll_alg_flag": ll_flag,
              "coll_alg_flag": coll_flag,
              "oll_alg_flag": oll_flag,
              "pll_alg_flag": pll_flag,
              "ell_alg_flag": ell_flag,
              "signature": signature(cube.stickers)}

    splits = split_note(notes)

    if splits is not None:
        bundle.update({"notes": splits})
    return bundle
