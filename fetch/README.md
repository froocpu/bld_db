# fetch

## What is this?

A Python module for making requests to the Google Sheets API and pulling data.

## TODO

- [ ] Sheet metadata and data:
    - [ ] How will it be stored?
    - [ ] How will it be queried?
    - [x] What metadata is necessary? What can we ignore and strip out?
    - [ ] How can we determine if a change has been made?
- [ ] Processed data:
    - [x] When algs are parsed, how will they be stored?
- [ ] People
    - [ ] Make deleting data easy.
    - [ ] Link to original sheets.
- [ ] Other data sources:
    - [x] [BH corners](http://www.speedcubing.com/chris/bhcorners.html)
    - [x] Best site ever (Roman)
    - [ ] AlgDB?
    
    
## What should it do?

- Snapshot sheets.
- Detect if a change has been made between one pass and the next. If change, store snapshot and delta.

