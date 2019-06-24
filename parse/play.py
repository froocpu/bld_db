
txt = "[U:[RDR',[M',U2]]][U' R' U, M2]"


def parenthetic_contents(string, ob="[", cb="]"):
    """
    Generate parenthesized contents in string as pairs (level, contents).
    https://stackoverflow.com/questions/4284991/parsing-nested-parentheses-in-python-grab-content-by-level
    :param string: cuber algorithm, concise notation.
    :type string: str
    :param ob: open bracket, the symbol to denote an starting point for the string. Usually '[' or '('.
    :type ob: str
    :param cb: closed bracket, the symbol to denote an ending point for the string. Usually ']' or ')'.
    :type cb: str
    :return: str
    """
    stack = []
    for i, c in enumerate(string):
        if c == ob:
            stack.append(i)
        elif c == cb and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])


def multiplier(string, m="*", op='(', cp=')'):
    """
    Parse parentheses and replicate it n times according to its multiplier, if one exists.
    :param string: raw algorithm
    :type string: str
    :param op: open parenthesis - symbol to denote the opener.
    :type op: str
    :param cp: closed parenthesis - symbol to denote the closer.
    :type cp: str
    :param m: the symbol to denote the multiplier
    :type m: str
    :return: str
    """
    empty = ""

    if m not in string:
        print("Multiplier notation is missing.")
        return empty
    splits = string.split(m)
    try:
        n = int(splits[1])
        cleaned = splits[0].replace(op, empty).replace(cp, empty)
        if n <= 0 or n > 10 or len(splits) != 2:
            print("Invalid multiplier notation.")
            return empty
        return cleaned * n
    except IndexError as e:
        print("Could not split using the multiplier provided.")





"""
While number of strings != 1:
    1. For the lowest levels:
        if commutator and conjugate:
            special edge case
        if commutator:
            expand A B A' B'
        else if conjugate:
            expand A B A'
        else
            nothing
    2. Replace parent levels string patterns with expanded variants.
    3. Remove children.

"""