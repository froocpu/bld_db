import pickle
import os.path
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
graham = '1-AnKGJMHN3SAOcZxem3XJ5tBm7Dk1dTRcZ7KcXYbGP4'
ollie = '15FmP089Qj9k8o9dFq3ZBm4cuBxs8exnf5e8WwXa4sZk'


def service_builder(creds):
    """
    Builds a spreadsheets service object.
    :param: creds - credentials
    :return: service object
    """
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()


def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def collect_sheets(sheets):
    """

    :param sheets:
    :return:
    """
    return [s.get("properties", {}).get("title") for s in sheets]



def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = authenticate()
    sheet = service_builder(creds=creds)

    SPREADSHEET_ID = ollie

    sheet_metadata = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()

    print(sheet_metadata.keys())
    for i in list(sheet_metadata.keys()):
        if isinstance(sheet_metadata[i], dict):
            print(sheet_metadata[i].keys())

    print(json.dumps(sheet_metadata))
    sheets = sheet_metadata.get('sheets', '')
    titles = collect_sheets(sheets)
    print(titles)

    for t in titles:
        RANGE_FORMAT = '{0}!{1}'
        RANGE_NAME = RANGE_FORMAT.format(t, 'A1:AZ200')

        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values')
        if not values:
            print('No data found.')
        else:
            print(values)


if __name__ == '__main__':
    main()
