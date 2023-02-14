#!/usr/bin/env python3
'''Defines BaseAuth class
'''
from api.v1.auth.auth import Auth
import re
from base64 import b64decode
from typing import Tuple, TypeVar
from models.base import Base
from models.user import User


class BasicAuth(Auth):
    '''Base for all basic auth jobs
    '''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        ''' returns the Base64 part of the
        Authorization header for a Basic Authentication:
        '''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not bool(re.match(r'^Basic \w', authorization_header)):
            return None
        return authorization_header[6]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        '''returns the decoded value of a Base64
        string base64_authorization_header
        '''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            credent = b64decode(base64_authorization_header)
            return credent.decode('utf-8')
        except Exception:
            return

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                     str) -> Tuple[str, str]:
        '''returns the user email and
        password from the Base64 decoded value.
        '''
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        credent = decoded_base64_authorization_header.split(':')
        email = credent[0]
        credent.pop(0)
        pwd = ':'.join(credent)
        return (email, pwd)

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        User.load_from_file()
        if User.count() == 0:
            return
        if len(User.search({'email': user_email})) == 0:
            return
        for user in User.search({'email': user_email}):
            if user.is_valid_password(user_pwd):
                return user
        return

    def current_user(self, request=None) -> TypeVar('User'):
        '''overloads Auth and retrieves the User instance for a request:
        '''
        if request is None:
            return
        b64_auth = self.authorization_header(request)
        b64_credentials = self.extract_base64_authorization_header(b64_auth)
        credentials = self.decode_base64_authorization_header(b64_credentials)
        user_email, user_pwd = self.extract_user_credentials(credentials)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
