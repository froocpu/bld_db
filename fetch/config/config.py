class DataSelector:
    SHEET_PARENT_FIELDS_TO_REMOVE = ['conditionalFormats', 'filterViews', 'basicFilter', 'sortSpecs', 'merges']
    SHEET_CHILD_FIELDS_TO_REMOVE = ['gridProperties', 'hidden']
    PROPERTIES_FIELDS_TO_REMOVE = ['autoRecalc', 'defaultFormat']
    # For each sheet, what range of cells should we request data from?
    DEFAULT_RANGE = 'A1:AZ1000'
    ALG_CHAR_MAX_LENGTH = 70
    ALG_CHAR_MIN_LENGTH = 6
    # How many spaces should each line be indented in the output JSON files?
    PRETTY_INDENT = 2
    NO_INDENT = True
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    MAX_ALLOWED_UNSOLVED_EDGES = 6
    MAX_ALLOWED_UNSOLVED_CORNERS = 5


class JobConfiguration:
    SECONDS_TO_WAIT = 13
    SHEETS_LIST_LOCATION = "../data/sheets_to_scan.txt"
    BH_CORNERS_LOCATION = "../data/bh.txt"
    OUTPUT_SINGLE_FILE = True