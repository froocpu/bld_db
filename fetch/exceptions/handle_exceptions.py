from parse.exceptions import *
from cube import AlgorithmDoesNothingException, TooManyUnsolvedPiecesException


def etl_exceptions(e, ind):
    """
    Check against a bunch of known exceptions and return a dictionary based on the result.
    :param e: Exception
    :param ind: index of the cell checked.
    :return: dict
    """
    failure_message = {"failure_description": str(e), "index": ind}
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
