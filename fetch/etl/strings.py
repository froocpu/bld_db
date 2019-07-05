from parse import Notation


def signature(array):
    """
    Convert the array into a string to be used as an identifier.
    Remove all non-numeric characters.
    :param array: cube.stickers
    :type array: numpy array
    :return: str
    """
    array_str = str(array.tolist())
    return array_str.replace(" ", Notation.EMPTY)\
        .replace("\n", Notation.EMPTY).replace("[", Notation.EMPTY).replace("]", Notation.EMPTY)\
        .replace(",", Notation.EMPTY)


def split_notes(notes):
    """
    Split notes up by line feeds and remove empty strings.
    :param notes: string containing notes from a cell
    :type notes: str
    :return: str
    """
    if notes is None or notes == Notation.EMPTY:
        return None
    splits = notes.split('\n')
    if len(splits) == 0:
        return None
    if isinstance(splits, list) and len(splits) == 1:
        return splits[0]
    if isinstance(splits, str):
        return splits
    return list(filter(None, splits))