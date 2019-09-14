from googleapiclient.discovery import build


def service_builder(credentials):
    """
    Builds a spreadsheets service object.
    :param: creds - credentials
    :return: service object
    """
    service = build("sheets", "v4", credentials=credentials)
    return service.spreadsheets()
