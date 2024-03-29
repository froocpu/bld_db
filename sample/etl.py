from fetch import write_json, prepare_data, trim_properties_metadata, trim_sheets_metadata, authenticate, service_builder

from time import sleep

import csv


if __name__ == '__main__':

    # Get credentials.json and authenticate the session, then initialise the service connection.
    credentials = authenticate()
    sheet = service_builder(credentials=credentials)

    with open("../config/sheets_to_scan.txt", "r") as txt:
        sheets_to_extract = csv.reader(txt, delimiter=',')
        next(sheets_to_extract)
        for row in sheets_to_extract:

            print("Collecting {}'s data...".format(row[1]))

            # Get metadata and trim it.
            sheet_metadata = sheet.get(spreadsheetId=row[0]).execute()
            trim_properties_metadata(sheet_metadata)
            trim_sheets_metadata(sheet_metadata)

            # Get the rest of the data and trim it.
            final_data = prepare_data(sheet, sheet_metadata)

            # Write it out to a file.
            # write_json(sheet_metadata, "data/metadata.json")
            filename = row[1].lower().encode('ascii', errors='ignore').decode('utf-8').replace(" ", "_")
            fn = "../data/json/{}.json".format(filename)

            

            print("Writing out to {}...".format(fn))
            write_json(final_data, fn)

            sec = 6
            print("Sleeping for {} seconds to avoid the rate limit:".format(sec))
            sleep(sec)






