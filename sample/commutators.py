import parse
import cube


if __name__ == "__main__":

    # Create a fresh cube.
    edges = cube.Cube(3)

    # Apply an edge commutator.
    comm = "[R':(f2 R2 U' R2)*2]"
    comm_alg = parse.Algorithm(comm)
    print(comm_alg.alg())

    edges.apply(comm_alg.alg())

    # Render an image of the cube to show that it's executed a 3-cycle.
    dpi = 865 / edges.nxnxn
    edges.render(flat=False).savefig("png/edge_commutator.png", dpi=dpi)
