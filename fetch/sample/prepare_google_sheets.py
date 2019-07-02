from fetch.session import authenticate, service_builder
from fetch.etl import write_json, prepare_data, trim_properties_metadata, trim_sheets_metadata, prepare_data_try_parse
from fetch.config import JobConfiguration

from time import sleep

import csv


if __name__ == '__main__':

    # Get credentials.json and authenticate the session, then initialise the service connection.
    credentials = authenticate()
    sheet = service_builder(credentials=credentials)

    with open(JobConfiguration.SHEETS_LIST_LOCATION, "r") as txt:
        sheets_to_extract = csv.reader(txt, delimiter=',')
        next(sheets_to_extract)
        for row in sheets_to_extract:

            print("Collecting {}'s data...".format(row[1]))

            # Get metadata and trim it.
            sheet_metadata = sheet.get(spreadsheetId=row[0]).execute()
            trim_properties_metadata(sheet_metadata)
            trim_sheets_metadata(sheet_metadata)

            # Get the rest of the data and trim it.
            final_data = prepare_data_try_parse(sheet, sheet_metadata)

            # Write it out to a file.
            # write_json(sheet_metadata, "data/metadata.json")
            filename = row[1].lower().encode('ascii', errors='ignore').decode('utf-8').replace(" ", "_")
            fn = "../data/json/{0}_{1}.json".format(filename, row[0][0:7])

            print("Writing out to {}...".format(fn))
            write_json(final_data, fn)

            print("Sleeping for {} seconds to avoid the rate limit:".format(JobConfiguration.SECONDS_TO_WAIT))
            sleep(JobConfiguration.SECONDS_TO_WAIT)





