def count_occurrences(pattern, s):
    """
    Count the number of occurrences of a string pattern in a string.
    :param pattern: str
    :param s: str
    :return: int
    """
    s_len = len(s)
    return (s_len - (len(s.replace(pattern, "")))) / len(pattern)


def remove_redundant_chars(start, end, s):
    """
    Remove redundant starting and ending characters that don't get used to parse grammar.
    :param start: first char
    :param end: last char
    :param s: string
    :return: str
    """
    while s.startswith(start) and s.endswith(end):
        s = s[1:len(s)-1]
        s = s.strip()
    return s


def clean_alg(alg):
    """
    A simple cleaning function. Algs don't need whitespace to be parsed.
    :param alg: raw string.
    :return: str
    """
    clean_ws = alg.strip().replace(" ", "")
    while (clean_ws.startswith("[") and clean_ws.endswith("]")) or (clean_ws.startswith("(") and clean_ws.endswith(")")):
        clean_ws = remove_redundant_chars("[", "]", remove_redundant_chars("(", ")", clean_ws))
    return clean_ws