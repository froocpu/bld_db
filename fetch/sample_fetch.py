from fetch.session import authenticate, service_builder
from fetch.etl import write_json, prepare_data, trim_properties_metadata, trim_sheets_metadata


if __name__ == '__main__':

    id = '15FmP089Qj9k8o9dFq3ZBm4cuBxs8exnf5e8WwXa4sZk'  # Ollie Frost's

    # Get credentials.json and authenticate the session.
    credentials = authenticate()

    # Initialise the service connection.
    sheet = service_builder(credentials=credentials)

    # Get metadata and trim it.
    sheet_metadata = sheet.get(spreadsheetId=id).execute()
    trim_properties_metadata(sheet_metadata)
    trim_sheets_metadata(sheet_metadata)

    # Get the rest of the data and trim it.
    final_data = prepare_data(sheet, sheet_metadata)

    # Write it out to files.
    write_json(sheet_metadata, "data/metadata.json")
    write_json(final_data, "data/data.json")
