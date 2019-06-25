def count_occurrences(pattern, s):
    """
    Count the number of occurrences of a string pattern in a string.
    :param pattern: str
    :param s: str
    :return: int
    """
    s_len = len(s)
    return (s_len - (len(s.replace(pattern, "")))) / len(pattern)


def clean_alg(alg):
    """
    A simple cleaning function. Algs don't need whitespace to be parsed.
    :param alg: unicode string containing algorithm
    :type alg: str
    :return: str
    """
    return alg.strip().replace(" ", "")