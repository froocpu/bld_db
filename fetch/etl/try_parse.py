from ..config import DataSelector
from .extract_metadata import collect_field
from .data_prep import signature

from parse import Algorithm
from parse.exceptions import *

from cube import Cube


def prepare_data_try_parse(sheet, meta):
    """
    Extract the real data from the original sheet object, using metadata as a guide, but also try and parse the algs.
    :param sheet: output from service_builder.
    :param meta: metadata about the sheet.
    :type meta: dict
    :return: dict
    """
    sheets = meta.get('sheets', '')
    titles = collect_field(sheets, "title")
    sheet_ids = collect_field(sheets, "sheetId")

    final_data = {"id": meta['spreadsheetId'], "spreadsheet_metadata": meta}
    sheet_contents = {}

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
        for ind, col in enumerate(values):
            cells = [cell for cell in col if
                     len(cell) > DataSelector.ALG_CHAR_MIN_LENGTH and len(cell) <= DataSelector.ALG_CHAR_MAX_LENGTH]
            if len(cells) > 0:
                successes = []
                failures = []
                for cell in cells:
                    try:
                        alg = Algorithm(cell)
                        cube = Cube(3)
                        cube.apply(alg.alg())
                        if cube.unsolved_corner_count > 5 or cube.unsolved_edge_count > 6:
                            continue
                        successes.append({"original": cell,
                                          "unsolved_corners": cube.unsolved_corner_count,
                                          "unsolved_edges": cube.unsolved_edge_count,
                                          "signature": signature(cube.stickers)})
                    except AmbiguousStatementException:
                        failures.append({"original": cell, "failure_reason": 0})
                    except BadMultiplierException:
                        failures.append({"original": cell, "failure_reason": 1})
                    except InvalidMoveException:
                        failures.append({"original": cell, "failure_reason": 2})
                    except BadSeparatorException:
                        failures.append({"original": cell, "failure_reason": 3})
                    except EmptyAlgorithmException:
                        failures.append({"original": cell, "failure_reason": 4})
                    except UnclosedBracketsException:
                        failures.append({"original": cell, "failure_reason": 5})
                    except InvalidSequenceException:
                        failures.append({"original": cell, "failure_reason": 6})
                    except Exception:
                        failures.append({"original": cell, "failure_reason": 7})

                filtered.update({ind: {"cells": cells, "successes": successes, "failures": failures}})

        # Start building the final dictionary.
        sheet_contents.update({int(sheet_ids[i]): {"range": result['range'],
                                                   "values": filtered}})

    final_data.update({"data": sheet_contents})

    return final_data
