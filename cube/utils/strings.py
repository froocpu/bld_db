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
