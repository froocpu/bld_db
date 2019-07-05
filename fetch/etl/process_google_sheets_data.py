from ..config import DataSelector
from .data_prep import collect_field, init_objects
from .analysis import analyze

from parse.exceptions import *
from cube.exceptions import *
from fetch.exceptions import failure_message_builder
from fetch.etl import split_note


def prepare_data(sheet, meta, notes):
    """
    Extract the real data from the original sheet object, using metadata as a guide, but also try and parse the algs.
    :param sheet: output from service_builder.
    :param meta: metadata about the sheet.
    :type meta: dict
    :param notes: notes from each cell - may contain alternate algs or notes.
    :type notes: dict
    :return: dict
    """
    sheets = meta.get('sheets', '')
    titles = collect_field(sheets, "title")
    sheet_ids = collect_field(sheets, "sheetId")

    final_data = {"id": meta['spreadsheetId'], "spreadsheet_metadata": meta}

    sheet_contents = {}
    successes = []
    failures = []

    for i, t in enumerate(titles):

        # Define the range to query (needs the name of the sheet.)
        sheet_range = '{0}!{1}'.format(t, DataSelector.DEFAULT_RANGE)
        result = sheet.values().get(spreadsheetId=meta['spreadsheetId'], range=sheet_range).execute()

        values = result.get('values')
        if not values:
            print("No data found in this sheet: {}".format(t))
            continue

        filtered = {}

        # Filter out cells with strings that are either too short or too long.
        for ind, column in enumerate(values):

            if len(column) > 0:

                cells = []

                for cell_ind, cell in enumerate(column):
                    # Don't do work if the string doesn't even match the legal limits.
                    if len(cell) <= DataSelector.ALG_CHAR_MIN_LENGTH or len(cell) > DataSelector.ALG_CHAR_MAX_LENGTH:
                        continue

                    # Prepare basic object.
                    cell_output = {"index": cell_ind,
                                   "row_index": cell_ind + 1,
                                   "column_index": int(ind) + 1,
                                   "text": cell}

                    # Google Sheets API is bad for returning notes data - not all the fields are returned.
                    # Quite a crappy try-catch, but if it can find anything at that index, then return it.
                    try:
                        this_note = notes['sheets'][i]['data'][0]['rowData'][ind]['values'][cell_ind]['note']
                    except (IndexError, KeyError):
                        this_note = None

                    # Process notes in separate try catch.
                    # If no notes, crack on.
                    if this_note is not None:
                        cell_output.update({"notes": this_note})
                        split_notes = split_note(this_note)
                        for note in split_notes:
                            try:
                                note_cube, note_alg = init_objects(input_alg=note)
                                note_bundle = analyze(note_cube)
                                note_bundle.update({"cell_index": cell_ind,
                                                    "row_index": cell_ind+1,
                                                    "column_index": ind,
                                                    "sheet_index": i,
                                                    "cleaned_text": "".join(note_alg.alg()),
                                                    "is_note_flag": True})
                                successes.append(note_bundle)
                            except (AmbiguousStatementException, BadMultiplierException, InvalidMoveException,
                                    BadSeparatorException, UnclosedBracketsException, InvalidSequenceException,
                                    AlgorithmDoesNothingException, TooManyUnsolvedPiecesException,
                                    IllegalCharactersException) as e:
                                failure_message = failure_message_builder(e=e, ind=cell_ind, sheet_index=i,
                                                                          alg_text=note, is_note_flag=True)
                                failures.append(failure_message)
                            except (EmptyAlgorithmException, Exception) as e:
                                if isinstance(e, Exception):
                                    print("{0} returned exception: {1}".format(note, e))
                                continue
                    # Continue processing the main data.
                    try:
                        cells.append(cell_output)
                        cube, alg = init_objects(input_alg=cell)
                        bundle = analyze(cube)
                        bundle.update({"cell_index": cell_ind,
                                       "row_index": cell_ind + 1,
                                       "cleaned_text": "".join(alg.alg()),
                                       "column_index": ind,
                                       "sheet_index": i
                                       })
                        successes.append(bundle)
                    except (AmbiguousStatementException, BadMultiplierException, InvalidMoveException,
                            BadSeparatorException, UnclosedBracketsException, InvalidSequenceException,
                            AlgorithmDoesNothingException, TooManyUnsolvedPiecesException, IllegalCharactersException) as e:
                        failure_message = failure_message_builder(e=e, ind=cell_ind, sheet_index=i, alg_text=cell)
                        failures.append(failure_message)
                    except (EmptyAlgorithmException, Exception) as e:
                        # Not bothered about collecting data on empty strings. Print if uncaught exception.
                        if isinstance(e, Exception):
                            print("{0} returned exception: {1}".format(cell, e))
                        continue

                filtered.update({ind: {"cells": cells}})

        # Start building the final dictionary.
        sheet_contents.update({sheet_ids[i]: {"range": result['range'], "cells": filtered}})

    final_data.update({"raw": sheet_contents, "algorithms": successes, "failures": failures})

    return final_data
