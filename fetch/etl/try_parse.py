from ..config import DataSelector
from .data_prep import collect_field, init_cube
from .analysis import analyze

from parse.exceptions import *
from cube.exceptions import *
from fetch.exceptions import etl_exceptions

from json import dumps


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

    print("full JSON: {}".format(dumps(notes)))
    print("notes len: {}".format(len(notes['sheets'])))
    print("sheets len: {}".format(len(titles)))

    for i, t in enumerate(titles):

        # Define the range to query (needs the name of the sheet.)
        sheet_range = '{0}!{1}'.format(t, DataSelector.RANGE)
        result = sheet.values().get(spreadsheetId=meta['spreadsheetId'], range=sheet_range).execute()

        values = result.get('values')
        if not values:
            print("No data found in this sheet: {}".format(t))
            continue

        filtered = {}

        # Filter out cells with strings that are either too short or too long.
        for ind, column in enumerate(values):

            if len(column) > 0:

                successes = []
                failures = []
                cells = []

                """
                if empty, then no values to parse. else, it should match?
                """

                for cell_ind, cell in enumerate(column):

                    try:
                        this_note = notes['sheets'][i]['data'][0]['rowData'][ind]['values'][cell_ind]['note']
                    except (IndexError, KeyError):
                        this_note = None

                    cell_output = {"index": ind,
                                  "row_index": cell_ind + 1,
                                  "column_index": int(ind) + 1,
                                  "text": cell}

                    if this_note is not None:
                        cell_output.update({"notes": this_note})

                    cells.append(cell_output)

                    if len(cell) <= DataSelector.ALG_CHAR_MIN_LENGTH or len(cell) > DataSelector.ALG_CHAR_MAX_LENGTH:
                        continue
                    try:
                        cube, alg = init_cube(input_alg=cell)
                        bundle = analyze(cube, this_note)
                        bundle.update({"index": cell_ind, "cleaned_text": "".join(alg.alg())})
                        successes.append(bundle)
                    except (AmbiguousStatementException, BadMultiplierException, InvalidMoveException,
                            BadSeparatorException, UnclosedBracketsException, InvalidSequenceException,
                            AlgorithmDoesNothingException, TooManyUnsolvedPiecesException, IllegalCharactersException) as e:
                        failure_message = etl_exceptions(e, cell_ind)
                        failures.append(failure_message)
                    except (EmptyAlgorithmException, Exception) as e:
                        # Not bothered about collecting data on empty strings. Print if uncaught exception.
                        if isinstance(e, Exception):
                            print("{0} returned exception: {1}".format(cell, e))
                        continue

                filtered.update({ind: {"cells": cells, "successes": successes, "failures": failures}})

        # Start building the final dictionary.
        sheet_contents.update({sheet_ids[i]: {"range": result['range'], "values": filtered}})

    final_data.update({"data": sheet_contents})

    return final_data
