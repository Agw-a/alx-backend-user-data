#!/usr/bin/env python3
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """returns the log message obfuscated:

    Args:
        field (List[str]): list of strings representing all fields to obfuscate
        redaction (str): string representing what field will be obfuscated
        message (str): string representing the log line
        separator (str): tring representing by which character is
        separating all fields in the log line (message)

    Returns:
        str: obfuscated string
    """
    for field in fields:
        message = re.sub(fr'{field}=[^{separator}]*',
                         f'{field}={redaction}', message)
    return message
