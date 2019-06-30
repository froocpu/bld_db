import parse
import cube


if __name__ == "__main__":
    # Create two fresh cubes, a 4x4x4 and a 3x3x3, because why not.
    corners = cube.Cube(4)
    edges = cube.Cube(3)

    # Apply a corner commutator.
    comm = "[U : [R D R' , U]]"
    comm_alg = parse.Algorithm(comm)
    print(comm_alg.alg())

    corners.apply(comm_alg.alg())

    # Render an image of the cube to show that it's executed a 3-cycle.
    # TODO: this fails, lol. y tho.
    dpi = 865 / corners.nxnxn
    corners.render(flat=False).savefig("png/corner_commutator.png", dpi=dpi)

    # Apply an edge commutator.
    comm = "R' f2 R2 U' R2 f2 R2 U' R'"
    comm_alg = parse.Algorithm(comm)
    print(comm_alg.alg())

    edges.apply(comm_alg.alg())

    # Render an image of the cube to show that it's executed a 3-cycle.
    dpi = 865 / edges.nxnxn
    edges.render(flat=False).savefig("png/edge_commutator.png", dpi=dpi)
