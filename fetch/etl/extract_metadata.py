def collect_field(sheets, field, parent="properties"):
    """
    Helper function. From the dict containing sheet data, extract all fields of a certain type.
    Typically used for extracting properties data.
    :param sheets: dict containing sheets data
    :type sheets: dict
    :param field: the name of the field to extract.
    :type field: str
    :param parent: (optional) the parent level JSON field to extract from.
    :type parent: str
    :return: list(str)
    """
    return [s.get(parent, {}).get(field) for s in sheets]