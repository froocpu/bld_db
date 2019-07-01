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
