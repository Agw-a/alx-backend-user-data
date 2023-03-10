#!/usr/bin/env python3
'''Personal data module
'''
import re
from typing import List
import logging
from mysql.connector.connection import MySQLConnection
import os

PII_FIELDS = (
    "name",
    "email",
    "phone",
    "ssn",
    "password"
)


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


class RedactingFormatter(logging.Formatter):
    '''Redacting Formatter class
    '''
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''initialize variables
        '''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = list(fields)

    def format(self, record: logging.LogRecord) -> str:
        '''Filters values in incoming logs
        '''
        msgs = super(RedactingFormatter, self).format(record)
        filters = filter_datum(self.fields, self.REDACTION,
                               msgs, self.SEPARATOR)
        return filters


def get_logger() -> logging.Logger:
    '''returns logging.Logger object
    '''
    logger = logging.getLogger('user_data')
    handle = logging.StreamHandler()
    handle.setLevel(logging.INFO)
    formats = RedactingFormatter(PII_FIELDS)
    handle.setFormatter(formats)
    logger.addHandler(handle)
    return logger


def get_db() -> MySQLConnection:
    ''' Returns a secure DB connection
    '''
    connection = MySQLConnection(
        host=os.getenv("PERSONAL_DATA_DB_HOST"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD")
    )

    return connection


def main() -> None:
    '''
    The function will obtain a database connection using get_db
    and retrieve all rows in the users table
    and display each row under a filtered format like this
    '''
    database = get_db()
    cursor = database.cursor()
    query = '''SELECT name, email, phone, ssn, password,
              ip, last_login, user_agent FROM users'''
    cursor.execute(query)
    response = cursor.fetchall()
    col = ('name', 'email', 'phone', 'ssn', 'password',
            'ip', 'last_login', 'user_agent')
    logger = get_logger()
    for ro in response:
        msg = ['{}={};'.format(col[i], ro[i]) for i in range(len(ro))]
        msg = ''.join(msg)
        lg = logging.LogRecord("user_data", logging.INFO, None,
                               None, msg, None, None)
        logger.handle(lg)
    database.close()


if __name__ == '__main__':
    main()
