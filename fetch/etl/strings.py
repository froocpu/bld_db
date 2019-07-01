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


def rotate_sticker(st, cw=None):
    """
    Given a sticker location, rotate it clockwise or anti-clockwise if it's a corner sticker, else flip it.
    :param st: string representing sticker
    :param st: str
    :param cw: if True, then rotate the sticker clockwise. If False, then counter clockwise. If None, assume it's an edge.
    :type cw: bool
    :return: str
    """

    if len(st) not in [2, 3]:
        return None
    if cw is None and len(st) == 2:
        return st[::-1].upper()
    if cw:
        return ''.join([st[1], st[2], st[0]]).upper()
    return ''.join([st[2], st[0], st[1]]).upper()
