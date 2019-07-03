from .strings import signature


def analyze(cube):
    """
    Perform cycle discovery on the cube and calculate metadata about the alg.
    :param cube: Cube object with moves applied.
    :type cube: Cube
    :return: a dict containing the results
    """
    edge_cycles = cube.edge_cycle_discovery()
    corner_cycles = cube.corner_cycle_discovery()

    flipped_edge_count = len([j for j in edge_cycles if len(j) == 1])
    twisted_corner_count = len([j for j in corner_cycles if len(j) == 1])

    parity_calculation = sum([len(targets) - 1 for targets in edge_cycles]) % 2
    parity_flag = (True if parity_calculation == 1 and flipped_edge_count == 0 else False)

    return {"edge_cycles": edge_cycles,
            "corner_cycles": corner_cycles,
            "unsolved_edges_count": cube.unsolved_edge_count,
            "unsolved_corners_count": cube.unsolved_corners,
            "flipped_edges_count": flipped_edge_count,
            "twisted_corners_count": twisted_corner_count,
            "parity_flag": parity_flag,
            "signature": signature(cube.stickers)}