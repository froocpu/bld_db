from json import dump, dumps
from ..config import DataSelector, JobConfiguration
from .extract_metadata import collect_field
from parse import Algorithm
from cube import Cube, TooManyUnsolvedPiecesException, AlgorithmDoesNothingException


def prepare_data(sheet, meta):
    """
    Extract the real data from the original sheet object, using metadata as a guide.
    :param sheet: output from service_builder.
    :param meta: metadata about the sheet.
    :type meta: dict
    :return: dict
    """
    sheets = meta.get("sheets", "")
    titles = collect_field(sheets, "title")
    sheet_ids = collect_field(sheets, "sheetId")

    final_data = {"id": meta["spreadsheetId"], "spreadsheet_metadata": meta}
    sheet_contents = {}

    for i, t in enumerate(titles):

        # Define the range to query (needs the name of the sheet.)
        sheet_range = "{0}!{1}".format(t, DataSelector.DEFAULT_RANGE)
        result = (
            sheet.values()
            .get(spreadsheetId=meta["spreadsheetId"], range=sheet_range)
            .execute()
        )

        values = result.get("values")
        if not values:
            print("No data found in this sheet: {}".format(t))
            continue

        filtered = {}

        # Filter out cells with strings that are either too short or too long.
        for ind, col in enumerate(values):
            cells = [
                cell
                for cell in col
                if len(cell) > DataSelector.ALG_CHAR_MIN_LENGTH
                and len(cell) <= DataSelector.ALG_CHAR_MAX_LENGTH
            ]
            if len(cells) > 0:
                filtered.update({ind: cells})

        # Start building the final dictionary.
        sheet_contents.update(
            {int(sheet_ids[i]): {"range": result["range"], "values": filtered}}
        )

    final_data.update({"data": sheet_contents})

    return final_data


def trim_properties_metadata(data, parent="properties"):
    """
    Strip out fields that aren't necessary, usually stuff like formatting.
    :param data: sheet metadata
    :type data: dict
    :param parent: the name of the properties field.
    :type parent: str
    :return: dict
    """
    for col in DataSelector.PROPERTIES_FIELDS_TO_REMOVE:
        data[parent].pop(col, None)
    return data


def trim_sheets_metadata(data, parent="sheets", child="properties"):
    """
    Strip out fields that aren't necessary from individual sheets, usually stuff like sorting specs and views.
    :param data: sheet metadata
    :type data: dict
    :param parent: the name of the sheets field.
    :type parent: str
    :param child: the name of the field inside the parent field from which to remove stuff.
    :type child: str
    :return: dict
    """
    for ind, j in enumerate(data[parent]):
        for col in DataSelector.SHEET_PARENT_FIELDS_TO_REMOVE:
            if col in data[parent][ind].keys():
                data[parent][ind].pop(col, None)
        if data[parent][ind][child]:
            for inner_col in DataSelector.SHEET_CHILD_FIELDS_TO_REMOVE:
                if inner_col in data[parent][ind][child].keys():
                    data[parent][ind][child].pop(inner_col)

    return data


def write_json(data, fn, append=JobConfiguration.OUTPUT_SINGLE_FILE):
    """
    Provide data and a file name and this function will create a formatted JSON file for you.
    :param data: sheets data to write to a file.
    :type data: dict
    :param fn: file name to write to.
    :type fn: str
    :param append: Write to one file or not.
    :type append: boolean
    :return: None
    """
    if append:
        # will overwrite DataSelector.PRETTY_INDENT
        with open(fn, "a+") as single_file:
            single_file.write(dumps(data) + "\n")
    else:
        with open(fn, "w") as dt:
            if DataSelector.NO_INDENT:
                dump(data, dt)
            else:
                dump(data, dt, indent=DataSelector.PRETTY_INDENT)


def init_objects(input_alg):
    """
    Initialise a cube, apply the algorithm to it and then for a second time to get to the correct state.
    :param input_alg: string containing an algorithm to parse.
    :type input_alg: str
    :return: Cube, Algorithm
    """
    cube = Cube(3)
    alg = Algorithm(input_alg)
    cube.apply(alg.alg())

    if (
        cube.unsolved_corner_count >= DataSelector.MAX_ALLOWED_UNSOLVED_CORNERS
        or cube.unsolved_edge_count >= DataSelector.MAX_ALLOWED_UNSOLVED_EDGES
    ):
        raise TooManyUnsolvedPiecesException(
            "This algorithm leaves a lot of pieces unsolved. The parser may be behaving incorrectly, or the alg is bad."
        )

    if cube.unsolved_corner_count + cube.unsolved_edge_count == 0:
        raise AlgorithmDoesNothingException("This algorithm appears to do nothing.")

    return cube, alg
