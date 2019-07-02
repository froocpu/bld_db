# cube (originally from Magic Cube)

## Original authors of MagicCube

- **David W. Hogg** (NYU)
- **Jacob Vanderplas** (UW)

## What is this?

### Problem to solve

There is a lot of variation between BLD solvers' sheets:

- Different buffers for all piece sets.
- Layout and formatting choices.
- Lists may not be complete - reader left to infer an alg from the inverse when it is not present.
- Different naming conventions, different syntax.

The combination of all of these factors makes writing a single set of rules for scraping data and consolidating it into a single location difficult to implement and scale.

### Solution

Given that we can scrape and parse text from spreadsheets into a set of moves, we can apply these moves to a representation of a cube and see what's changed. So for example, Alice has this alg in her sheet somewhere:

`[M', U2]`

This will be translated to:

`["M'", "U2", "M", "U2"]`

The resulting 3-cycles will look something like:

```
UF -> UB -> DF // or
UB -> DF -> UF // or
DF -> UF -> UB
```

If we use the other sticker as a reference, we have three more potential 3-cycles:

```
FU -> BU -> FD // or
BU -> FD -> FU // or
FD -> FU -> BU
```

However, `print(Cube.stickers)` will return this nested array:

    [[[0 0 0]
      [0 0 1]
      [0 0 0]]
    
     [[1 1 1]
      [1 1 0]
      [1 1 1]]
    
     [[2 2 2]
      [2 2 3]
      [2 2 2]]
    
     [[3 3 3]
      [3 3 2]
      [3 3 3]]
    
     [[4 4 4]
      [4 4 4]
      [4 4 4]]
    
     [[5 5 5]
      [5 5 5]
      [5 5 5]]]

This signature is unique to that cube state, regardless of the alg that takes you there.

What this means is that as long as the lists of arrays are stored, that it shouldn't matter what the user's buffer preferences or sticker naming conventions are. As long as they have the capacity to search for three pieces to cycle, then the database can return algs based on the delta that cube state would generate.

    GIVEN 
        that a user selects their starting buffer (or buffer sticker)
    AND 
        that user selects their next two targets for a commutator
    WHEN 
        they send the query to the database
    THEN 
        the stickers will be converted to a stickers signature
    AND 
        all of the algs matching that signature will be returned.

## TODO

- [ ] Write a wrapper for the `Cube` class:
    - [x] Configure the rendering properties.
    - [x] Create wrapper methods for M moves, S moves, E moves, rotations etc.
- [x] Decide on a method of storing and querying the deltas rather than individual algs.
- [ ] Image rendering:
    - [ ] What images should be rendered for each case?
    - [ ] Where to store these images?
    - [ ] Space, query time considerations.
- [ ] People:
    - [ ] Are permissions required?
    
    
## Notes

When `cube.stickers` is printed, use the following rotations to orient your cube in relation to the output (so that the face will be on U):

    0:U, 1:D, 2:F, 3:B, 4:R, 5:L

    U: y
    D: x2 y
    F: z x
    B: x' y'
    R: z' y2
    L: z
