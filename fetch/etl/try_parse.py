from ..config import DataSelector
from .extract_metadata import collect_field
from .strings import signature

from parse import Algorithm
from parse.exceptions import *

from cube import Cube, AlgorithmDoesNothingException, TooManyUnsolvedPiecesException


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
        for ind, column in enumerate(values):
            if len(column) > 0:
                successes = []
                failures = []
                cells = []

                for cell_ind, cell in enumerate(column):

                    cells.append({"index": ind,
                                  "row_index": cell_ind + 1,
                                  "column_index": int(ind) + 1,
                                  "text": cell
                                 })

                    if len(cell) <= DataSelector.ALG_CHAR_MIN_LENGTH or len(cell) > DataSelector.ALG_CHAR_MAX_LENGTH:
                        continue
                    try:

                        alg = Algorithm(cell)
                        cube = Cube(3)
                        cube.apply(alg.alg())

                        if cube.unsolved_corner_count >= DataSelector.MAX_ALLOWED_UNSOLVED_CORNERS or cube.unsolved_edge_count >= DataSelector.MAX_ALLOWED_UNSOLVED_EDGES:
                            raise TooManyUnsolvedPiecesException("This algorithm leaves a lot of pieces unsolved. The parser may be behaving incorrectly, or the alg is bad.")

                        if cube.unsolved_corner_count + cube.unsolved_edge_count == 0:
                            raise AlgorithmDoesNothingException("This algorithm appears to do nothing.")

                        edge_cycles = cube.edge_cycle_discovery()
                        corner_cycles = cube.corner_cycle_discovery()

                        flipped_edge_count = len([j for j in edge_cycles if len(j) == 1])
                        twisted_corner_count = len([j for j in corner_cycles if len(j) == 1])

                        parity_calculation = sum([len(targets) - 1 for targets in edge_cycles]) % 2

                        successes.append({"index": cell_ind,
                                          "cleaned_text": "".join(alg.alg()),
                                          "edge_cycles": edge_cycles,
                                          "corner_cycles": corner_cycles,
                                          "unsolved_corners_count": cube.unsolved_corner_count,
                                          "unsolved_edges_count": cube.unsolved_edge_count,
                                          "flipped_edges_count": flipped_edge_count,
                                          "twisted_corners_count": twisted_corner_count,
                                          "parity_flag": (True if parity_calculation == 1 and flipped_edge_count == 0 else False),
                                          "signature": signature(cube.stickers)})

                    except EmptyAlgorithmException:
                        # Not bothered about collecting data on empty strings.
                        continue
                    except AmbiguousStatementException as e:
                        failures.append({"original": cell_ind, "failure_code": 0, "failure_description": str(e)})
                    except BadMultiplierException as e:
                        failures.append({"original": cell_ind, "failure_code": 1, "failure_description": str(e)})
                    except InvalidMoveException as e:
                        failures.append({"original": cell_ind, "failure_code": 2, "failure_description": str(e)})
                    except BadSeparatorException as e:
                        failures.append({"original": cell_ind, "failure_code": 3, "failure_description": str(e)})
                    except UnclosedBracketsException as e:
                        failures.append({"original": cell_ind, "failure_code": 4, "failure_description": str(e)})
                    except InvalidSequenceException as e:
                        failures.append({"original": cell_ind, "failure_code": 5, "failure_description": str(e)})
                    except AlgorithmDoesNothingException as e:
                        failures.append({"original": cell_ind, "failure_code": 6, "failure_description": str(e)})
                    except TooManyUnsolvedPiecesException as e:
                        failures.append({"original": cell_ind, "failure_code": 7, "failure_description": str(e)})
                    except IllegalCharactersException as e:
                        failures.append({"original": cell_ind, "failure_code": 8, "failure_description": str(e)})
                    except Exception:
                        continue

                filtered.update({ind: {"cells": cells,
                                       "successes": successes,
                                       "failures": failures}})

        # Start building the final dictionary.
        sheet_contents.update({int(sheet_ids[i]): {"range": result['range'],
                                                   "values": filtered}})

    final_data.update({"data": sheet_contents})

    return final_data
