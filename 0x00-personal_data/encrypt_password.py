#!/usr/bin/env python3
'''password encryption/validation module
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''expects one string argument name password and
        returns a salted, hashed password, which is a byte string.
    '''
    slate = bcrypt.gensalt()
    pass_bytes = password.encode('utf-8')
    return bcrypt.hashpw(pass_bytes, slate)


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''validate that the provided password matches the hashed password.
    '''
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)
