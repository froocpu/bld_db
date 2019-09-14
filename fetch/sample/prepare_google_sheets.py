from fetch.session import authenticate, service_builder
from fetch.etl import (
    write_json,
    trim_properties_metadata,
    trim_sheets_metadata,
    prepare_data,
)  # , prepare csv
from fetch.config import JobConfiguration

from time import sleep, time
from json import dumps

import datetime
import hashlib
import csv


if __name__ == "__main__":

    # Get credentials.json and authenticate the session, then initialise the service connection.
    credentials = authenticate()
    sheet = service_builder(credentials=credentials)

    with open(JobConfiguration.SHEETS_LIST_LOCATION, "r") as txt:
        sheets_to_extract = csv.reader(txt, delimiter=",")
        next(sheets_to_extract)
        for row in sheets_to_extract:

            print("Collecting {}'s data...".format(row[1]))

            # Get metadata and trim it.
            sheet_metadata = sheet.get(spreadsheetId=row[0]).execute()
            sheet_notes = sheet.get(
                spreadsheetId=row[0], fields="sheets/data/rowData/values/note"
            ).execute()

            trim_properties_metadata(sheet_metadata)
            trim_sheets_metadata(sheet_metadata)

            # Get the rest of the data and trim it.
            final_data, failures = prepare_data(sheet, sheet_metadata, sheet_notes)

            # Append some extra fields.
            final_data.update(
                {
                    "author": row[1],
                    "timestamp_processed": datetime.datetime.fromtimestamp(
                        time()
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "md5sum": hashlib.md5(
                        dumps(final_data, sort_keys=True).encode("utf-8")
                    ).hexdigest(),
                }
            )

            filename = (
                row[1]
                .lower()
                .encode("ascii", errors="ignore")
                .decode("utf-8")
                .replace(" ", "_")
            )
            fn = "../data/json/all.json"
            failures_report_fn = "../data/json/failures.json"

            print("Writing out to {}...".format(fn))
            write_json(data=final_data, fn=fn)

            print("Writing failures report to {}...".format(failures_report_fn))
            write_json(data=failures, fn=failures_report_fn)

            print(
                "Sleeping for {} seconds to avoid the rate limit:".format(
                    JobConfiguration.SECONDS_TO_WAIT
                )
            )
            sleep(JobConfiguration.SECONDS_TO_WAIT)
