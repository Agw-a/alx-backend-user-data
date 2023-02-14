#!/usr/bin/env python3
"""
This module defines the class Auth
"""

from flask import request
from typing import List, TypeVar
import re


class Auth():
    '''authentication operations
    '''
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        '''checks if a resource requires auth.
        '''
        if path[len(path) - 1] != '/' and path[len(path) - 1] != '*':
            path += '/'
        for excluded_path in excluded_paths:
            if path[len(path) - 1] == '*':
                if bool(re.match(fr'^{excluded_path}\w*', path)):
                    return False
            if path in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''get and return auth header & request
        '''
        if request is None:
            return None
        return request.headers.get('Authaurization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''get and return current user object
        '''
        return None
