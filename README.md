# bld_db

## What is this?

All BLD algs in one place, automatically scraped and updated once a day.

## Where to start?

Hi Matt!

### Directories

- `/cube` - contains code for presenting a Rubik's cube in memory. This is required in order to:
    - Apply parsed sequences of moves to a cube and measure what's changed.
    - Render 3D PNG images of cubes for a front-end.
    - Create unique 'signatures' of cube states.
- `/db` - work in progress (WIP) for database stuff.
- `/fetch` - package for pulling data, extracting it, and storing it in a new file format.
- `/parse` - where the 'parsing algorithm' sits. See the examples in `/parse/sample` for examples.
