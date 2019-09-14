from parse.exceptions import *
from cube import AlgorithmDoesNothingException, TooManyUnsolvedPiecesException


def failure_message_builder(e, ind, alg_text, sheet_index, is_note_flag=False):
    """
    Check against a bunch of known exceptions and return a dictionary based on the result.
    :param e: Exception
    :param ind: index of the cell checked.
    :param alg_text: the failed text
    :param sheet_index: the id of the sheet.
    :param is_note_flag: whether the parsed text was a note or not.
    :return: dict
    """
    failure_message = {
        "cell_index": ind,
        "row_index": ind + 1,
        "sheet_index": sheet_index,
        "text": alg_text,
    }

    if is_note_flag:
        failure_message.update({"is_note_flag": is_note_flag})

    failure_code_key = "failure_code"
    if isinstance(e, AmbiguousStatementException):
        failure_message.update({failure_code_key: 0})
    elif isinstance(e, BadMultiplierException):
        failure_message.update({failure_code_key: 1})
    elif isinstance(e, InvalidMoveException):
        failure_message.update({failure_code_key: 2})
    elif isinstance(e, BadSeparatorException):
        failure_message.update({failure_code_key: 3})
    elif isinstance(e, UnclosedBracketsException):
        failure_message.update({failure_code_key: 4})
    elif isinstance(e, InvalidSequenceException):
        failure_message.update({failure_code_key: 5})
    elif isinstance(e, AlgorithmDoesNothingException):
        failure_message.update({failure_code_key: 6})
    elif isinstance(e, TooManyUnsolvedPiecesException):
        failure_message.update({failure_code_key: 7})
    elif isinstance(e, IllegalCharactersException):
        failure_message.update({failure_code_key: 8})

    return failure_message
