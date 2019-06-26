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
    Algs need to be stripped of all whitespace characters and forced to ascii encoding.
    :param alg: unicode string containing algorithm
    :type alg: str
    :return: str
    """
    empty = ""
    stripped = alg.strip().replace(" ", empty).replace("\t", empty).replace("\n", empty).replace("\r", empty)
    return stripped.encode('ascii', errors='ignore').decode('utf-8')