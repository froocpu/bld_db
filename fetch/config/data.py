class DataSelector:
    SHEET_FIELDS_TO_REMOVE = ['conditionalFormats', 'filterViews', 'basicFilter', 'sortSpecs']
    PROPERTIES_FIELDS_TO_REMOVE = ['autoRecalc', 'defaultFormat']
    # For each sheet, what range of cells should we request data from?
    RANGE = 'A1:AZ1000'
    ALG_CHAR_MAX_LENGTH = 100
    ALG_CHAR_MIN_LENGTH = 4
    # How many spaces should each line be indented in the output JSON files?
    PRETTY_INDENT = 2
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
