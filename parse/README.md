# TODO:

- [ ] Parse brackets. i.e. `(M' U M U)*2`
- [ ] Parse M2 notation. i.e. `[U' R' U: M2][U L U', M2]`
- [ ] Handle this case: `[R: R U R', D]` - both commutator and conjugate notation is allowed.

## Algorithm

- Normalise:
    - Remove all whitespace.
    - If chained (i.e. M2 alg like `[Alg A][Alg B]`) then split. Apply proceeding steps for each part or combine.
- Expand:
    - Round brackets:
        - If no multiplier, remove brackets.
        - Else, repeat pattern as many times as specified.
    - Square brackets:
        - If both commutator and conjugate notation, expand B part.
        - If simple commutator or conjugate notation, perform expansion.
        