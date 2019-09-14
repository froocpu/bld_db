from fetch.config import JobConfiguration, DataSelector
from fetch.etl import signature, write_json
from parse import Algorithm
from cube import Cube

from parse.exceptions import *
from cube.exceptions import *


if __name__ == "__main__":

    # Get credentials.json and authenticate the session, then initialise the service connection.
    with open(JobConfiguration.BH_CORNERS_LOCATION, "r") as txt:

        manual_id = "bhcorners"
        final_dataset = {"id": manual_id}

        # Read in algs.
        raw_algs = [i.replace("\n", "") for i in txt.readlines()]
        sheet_metadata = {
            "spreadsheetId": manual_id,
            "properties": {
                "title": "Beyer-Hardwick Corner Algorithms",
                "locale": "en_GB",
                "timeZone": None,
            },
            "spreadsheetUrl": "http://www.speedcubing.com/chris/bhcorners.html",
        }

        final_dataset.update(sheet_metadata)
        # Update the final data object.

        cells = []
        successes = []
        failures = []

        for ind, cell in enumerate(raw_algs):

            cells.append(
                {"index": ind, "row_index": ind + 1, "column_index": 2, "text": cell}
            )

            if (
                len(cell) <= DataSelector.ALG_CHAR_MIN_LENGTH
                or len(cell) > DataSelector.ALG_CHAR_MAX_LENGTH
            ):
                continue
            try:

                def init_cube(cell):
                    alg = Algorithm(cell)
                    cube = Cube(3)
                    cube.apply(alg.alg())
                    return alg, cube

                if (
                    cube.unsolved_corner_count
                    >= DataSelector.MAX_ALLOWED_UNSOLVED_CORNERS
                    or cube.unsolved_edge_count
                    >= DataSelector.MAX_ALLOWED_UNSOLVED_EDGES
                ):
                    raise TooManyUnsolvedPiecesException(
                        "This algorithm leaves a lot of pieces unsolved. The parser may be behaving incorrectly, or the alg is bad."
                    )

                if cube.unsolved_corner_count + cube.unsolved_edge_count == 0:
                    raise AlgorithmDoesNothingException(
                        "This algorithm appears to do nothing."
                    )

                edge_cycles = cube.edge_cycle_discovery()
                corner_cycles = cube.corner_cycle_discovery()

                flipped_edge_count = len([j for j in edge_cycles if len(j) == 1])
                twisted_corner_count = len([j for j in corner_cycles if len(j) == 1])

                parity_calculation = (
                    sum([len(targets) - 1 for targets in edge_cycles]) % 2
                )

                successes.append(
                    {
                        "index": ind,
                        "cleaned_text": "".join(alg.alg()),
                        "edge_cycles": edge_cycles,
                        "corner_cycles": corner_cycles,
                        "unsolved_corners_count": cube.unsolved_corner_count,
                        "unsolved_edges_count": cube.unsolved_edge_count,
                        "flipped_edges_count": flipped_edge_count,
                        "twisted_corners_count": twisted_corner_count,
                        "parity_flag": (
                            True
                            if parity_calculation == 1 and flipped_edge_count == 0
                            else False
                        ),
                        "signature": signature(cube.stickers),
                    }
                )

            except EmptyAlgorithmException:
                # Not bothered about collecting data on empty strings.
                continue
            except AmbiguousStatementException as e:
                failures.append(
                    {"original": ind, "failure_code": 0, "failure_description": str(e)}
                )
            except BadMultiplierException as e:
                failures.append(
                    {"original": ind, "failure_code": 1, "failure_description": str(e)}
                )
            except InvalidMoveException as e:
                failures.append(
                    {"original": ind, "failure_code": 2, "failure_description": str(e)}
                )
            except BadSeparatorException as e:
                failures.append(
                    {"original": ind, "failure_code": 3, "failure_description": str(e)}
                )
            except UnclosedBracketsException as e:
                failures.append(
                    {"original": ind, "failure_code": 4, "failure_description": str(e)}
                )
            except InvalidSequenceException as e:
                failures.append(
                    {"original": ind, "failure_code": 5, "failure_description": str(e)}
                )
            except AlgorithmDoesNothingException as e:
                failures.append(
                    {"original": ind, "failure_code": 6, "failure_description": str(e)}
                )
            except TooManyUnsolvedPiecesException as e:
                failures.append(
                    {"original": ind, "failure_code": 7, "failure_description": str(e)}
                )
            except IllegalCharactersException as e:
                failures.append(
                    {"original": ind, "failure_code": 8, "failure_description": str(e)}
                )
            except Exception:
                continue

        final_dataset.update(
            {
                "data": {
                    "0": {
                        "values": {
                            "0": {
                                "cells": cells,
                                "successes": successes,
                                "failures": failures,
                            }
                        }
                    }
                }
            }
        )

        write_json(final_dataset, "../data/json/bh.json")
