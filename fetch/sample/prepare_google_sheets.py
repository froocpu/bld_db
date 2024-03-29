from fetch.session import authenticate, service_builder
from fetch.etl import write_json, trim_properties_metadata, trim_sheets_metadata, prepare_data
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
            sheet_notes = sheet.get(spreadsheetId=row[0], fields="sheets/data/rowData/values/note").execute()

            trim_properties_metadata(sheet_metadata)
            trim_sheets_metadata(sheet_metadata)

            # Get the rest of the data and trim it.
            final_data = prepare_data(sheet, sheet_metadata, sheet_notes)

            # Write it out to a file.
            # write_json(sheet_metadata, "data/metadata.json")
            filename = row[1].lower().encode('ascii', errors='ignore').decode('utf-8').replace(" ", "_")
            #fn = "../data/json/{0}_{1}.json".format(filename, row[0][0:7])
            fn = "../data/json/all.json"

            print("Writing out to {}...".format(fn))
            write_json(data=final_data, fn=fn, append=True)

            print("Sleeping for {} seconds to avoid the rate limit:".format(JobConfiguration.SECONDS_TO_WAIT))
            sleep(JobConfiguration.SECONDS_TO_WAIT)






