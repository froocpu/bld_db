from json import dump
from ..config import DataSelector
from .extract_metadata import collect_field


def prepare_data(sheet, meta):
    """
    Extract the real data from the original sheet object, using metadata as a guide.
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
                filtered.update({ind: cells})

        # Start building the final dictionary.
        sheet_contents.update({int(sheet_ids[i]): {"range": result['range'],
                                                   "values": filtered}})

    final_data.update({"data": sheet_contents})

    return final_data


def trim_properties_metadata(data, parent='properties'):
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


def trim_sheets_metadata(data, parent='sheets'):
    """
    Strip out fields that aren't necessary from individual sheets, usually stuff like sorting specs and views.
    :param data: sheet metadata
    :type data: dict
    :param parent: the name of the sheets field.
    :type parent: str
    :return: dict
    """
    for ind in range(len(data[parent])):
        for col in DataSelector.SHEET_FIELDS_TO_REMOVE:
            data[parent][ind].pop(col, None)
    return data


def write_json(data, fn):
    """
    Provide data and a file name and this function will create a formatted JSON file for you.
    :param data: sheets data to write to a file.
    :type data: dict
    :param fn: file name to write to.
    :type fn: str
    :return: None
    """
    with open(fn, "w") as dt:
        dump(data, dt, indent=DataSelector.PRETTY_INDENT)


