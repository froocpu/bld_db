import parse
import cube


if __name__ == "__main__":
    # Create a representation of a 3x3x3 cube.
    cube = cube.Cube(3)

    # Apply a complicated looking algorithm for a T-perm.
    t_perm = "[R,U] R' (F R2 U' [R': U'] U) R' F'"
    t_alg = parse.Algorithm(t_perm)
    print(t_alg.alg())

    # Render an image of the cube to show that it's a T-perm.
    dpi = 865 / 3
    cube.apply(t_alg.alg())
    cube.render(flat=False).savefig("png/t_perm.png", dpi=dpi)

    # Apply the inverse alg and see if it's solved.
    cube.apply(t_alg.invert())
    cube.render(flat=False).savefig("png/solved.png", dpi=dpi)