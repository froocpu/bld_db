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


def split_note(note):
    """
    Split notes up by line feeds and remove empty strings.
    :param note: string containing notes from a cell
    :type note: str
    :return: str or list
    """
    if note is None or note == Notation.EMPTY:
        return None
    splits = note.split('\n')
    return list(filter(None, splits))
