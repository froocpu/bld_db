# bld_db

## parse

### What is this?

Parse is a Python module for manipulating strings of text and parsing speedsolving algorithms. Its key functions are to:

- Validate user input strings. For example, is the algorithm provided using valid notation?
- Parse raw text into a sequence of moves that can be manipulated.
- Provide functionality for inverting an alg, changing notation standards.

### Integration

When text is extracted from a BLD solver's Google Sheet repository, it will ultimately be parsed into a sequence of moves and stored as such in the database.

### Example

Here is an example usage:

```python
import parse as p

t_perm = p.Algorithm("[R,U] R' F R2 U' [R': U'] U R' F'")

print("Alg moves: {0}".format(t_perm.alg()))
# Alg moves: ['R', 'U', "R'", "U'", "R'", 'F', 'R2', "U'", "R'", "U'", 'R', 'U', "R'", "F'"]
print("Alg inverse: {0}".format(t_perm.invert()))
# Alg inverse: ['F', 'R', "U'", "R'", 'U', 'R', 'U', "R2'", "F'", 'R', 'U', 'R', "U'", "R'"]
```

## TODO:

- [x] Better sanitisation of user input. **This one is very important.** 
- [x] Some brackets get parsed as moves. i.e. `"[R,U] (R' F R2) U' [R': U'] U R' F'"` will break.
- [x] Should double moves always be displayed as primes when inverted? i.e. `R2'` and not `R2`
- [ ] Make preparations for scaling the project to larger cubes.
- [ ] Benchmark the performance of functions.
- [x] More tests, specifically on when to throw errors.
- [ ] Cancellations. i.e. `R2 R -> R'`
- [ ] Comments allowed in algs?
