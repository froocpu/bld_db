import json
import pandas as pd
import numpy as np

from pandas.io.json import json_normalize


fn = "../data/json/all.json"


def flatten(data, col):
    cols = ["author", "spreadsheetId"]
    df = json_normalize(data[col])
    for c in cols:
        df[c] = data[c]
    return df


def prepare_sheets(d):
    sheets = json_normalize(d["sheets"])
    sheets = sheets[["sheetId", "title"]]
    sheets["parent_id"] = d["spreadsheetId"]
    return sheets


def prepare_csv(fn):
    algs = pd.DataFrame(
        columns=[
            "edge_cycles",
            "corner_cycles",
            "unsolved_edges_count",
            "unsolved_corners_count",
            "flipped_edges_count",
            "twisted_corners_count",
            "parity_flag",
            "ll_alg_flag",
            "coll_alg_flag",
            "oll_alg_flag",
            "pll_alg_flag",
            "ell_alg_flag",
            "signature",
            "cell_index",
            "row_index",
            "column_index",
            "sheet_id",
            "original_text",
            "cleaned_text",
            "is_note_flag",
            "spreadsheetId",
        ]
    )

    with open(fn) as jsn:
        for i in jsn.readlines():
            txt = json.loads(i)
            algs = pd.concat([algs, flatten(txt, "algorithms")], sort=False)
            sheets = prepare_sheets(txt)

    # reorder
    algs = algs[
        [
            "author",
            "spreadsheetId",
            "sheet_id",
            "cell_index",
            "row_index",
            "column_index",
            "is_note_flag",
            "original_text",
            "cleaned_text",
            "edge_cycles",
            "corner_cycles",
            "unsolved_edges_count",
            "unsolved_corners_count",
            "flipped_edges_count",
            "twisted_corners_count",
            "parity_flag",
            "ll_alg_flag",
            "coll_alg_flag",
            "oll_alg_flag",
            "pll_alg_flag",
            "ell_alg_flag",
            "signature",
        ]
    ]

    algs = algs.rename(columns={"spreadsheetId": "id"})

    for col in [
        "ll_alg_flag",
        "coll_alg_flag",
        "oll_alg_flag",
        "pll_alg_flag",
        "ell_alg_flag",
        "is_note_flag",
        "parity_flag",
        "edge_cycles",
        "corner_cycles",
    ]:
        algs[col].replace(to_replace=True, value="Y", inplace=True)
        algs[col].replace(to_replace=False, value="N", inplace=True)
        algs[col].replace(to_replace=np.nan, value="N", inplace=True, regex=True)
        algs[col] = algs[col].apply(lambda y: "" if len(y) == 0 else y)

    algs.replace(to_replace=r"^\[\]$", regex=True, value=None, inplace=True)

    algs.to_csv("../data/json/algorithms.csv", index=False)


if __name__ == "__main__":
    df = pd.read_json(fn, lines=True)
    print(df.columns)
    prepare_csv(fn)
