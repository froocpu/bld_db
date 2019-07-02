from ..config import DataSelector
from .extract_metadata import collect_field
from .strings import signature

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
        for ind, cells in enumerate(values):
            if len(cells) > 0:
                successes = []
                failures = []
                for cell_ind, cell in enumerate(cells):
                    if len(cell) <= DataSelector.ALG_CHAR_MIN_LENGTH or len(cell) > DataSelector.ALG_CHAR_MAX_LENGTH:
                        continue
                    try:
                        alg = Algorithm(cell)
                        cube = Cube(3)
                        cube.apply(alg.alg())

                        if cube.unsolved_corner_count >= DataSelector.MAX_ALLOWED_UNSOLVED_CORNERS or cube.unsolved_edge_count >= DataSelector.MAX_ALLOWED_UNSOLVED_EDGES or (cube.unsolved_corner_count + cube.unsolved_edge_count == 0):
                            continue

                        edge_cycles = cube.edge_cycle_discovery()
                        corner_cycles = cube.corner_cycle_discovery()

                        flipped_edge_count = len([j for j in edge_cycles if len(j) == 1])
                        twisted_corner_count = len([j for j in corner_cycles if len(j) == 1])

                        successes.append({"original": cell_ind,
                                          "edge_cycles": edge_cycles,
                                          "corner_cycles": corner_cycles,
                                          "unsolved_corners_count": cube.unsolved_corner_count,
                                          "unsolved_edges_count": cube.unsolved_edge_count,
                                          "flipped_edges_count": flipped_edge_count,
                                          "twisted_corners_count": twisted_corner_count,
                                          "parity_flag": (True if flipped_edge_count % 2 == 0 and twisted_corner_count % 2 == 0 and twisted_corner_count == 0 and flipped_edge_count == 0 else False),
                                          "signature": signature(cube.stickers)})

                    except AmbiguousStatementException as e:
                        failures.append({"original": cell_ind, "failure_id": 0, "failure_description": str(e)})
                    except BadMultiplierException as e:
                        failures.append({"original": cell_ind, "failure_id": 1, "failure_description": str(e)})
                    except InvalidMoveException as e:
                        failures.append({"original": cell_ind, "failure_id": 2, "failure_description": str(e)})
                    except BadSeparatorException as e:
                        failures.append({"original": cell_ind, "failure_id": 3, "failure_description": str(e)})
                    except UnclosedBracketsException as e:
                        failures.append({"original": cell_ind, "failure_id": 4, "failure_description": str(e)})
                    except InvalidSequenceException as e:
                        failures.append({"original": cell_ind, "failure_id": 5, "failure_description": str(e)})
                    except EmptyAlgorithmException:
                        continue
                    except IllegalCharactersException as e:
                        failures.append({"original": cell_ind, "failure_id": 6, "failure_description": str(e)})
                    #except Exception as e:
                    #    failures.append({"original": cell, "failure_id": 7, "failure_description": str(e)})

                filtered.update({ind: {"cells": cells, "successes": successes, "failures": failures}})

        # Start building the final dictionary.
        sheet_contents.update({int(sheet_ids[i]): {"range": result['range'],
                                                   "values": filtered}})

    final_data.update({"data": sheet_contents})

    return final_data
