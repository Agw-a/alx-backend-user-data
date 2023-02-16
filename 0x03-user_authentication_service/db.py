#!/usr/bin/env python3
'''DB module
'''

from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
# import os

# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# connection_string = 'sqlite:///'+os.path.join(BASE_DIR, 'site.db')


class DB():
    '''DB Class
    '''
    def __init__(self) -> None:
        '''initialize a new DB engine
        '''
        # self._engine = create_engine(connection_string, echo=False)
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        '''Memoized session object
        '''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''Add and commit a user
        '''
        try:
            newUser = User(email=email, hashed_password=hashed_password)
            self._session.add(newUser)
            self._session.commit()
        except Exception:
            self._session.rollback()
            newUser = None
        return newUser

    def find_user_by(self, **kwargs) -> User:
        '''Returns first row found in users filtered by arguments
        '''
        fields, values = [], []
        for key, val in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(val)
            else:
                raise InvalidRequestError()
        res = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if res is None:
            raise NoResultFound()
        return res

    def update_user(self, user_id: int, **kwargs) -> None:
        '''locate a user based on id and update and commit to DB
        '''
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        updated = {}
        for key, val in kwargs.items():
            if hasattr(User, key):
                updated[getattr(User, key)] = val
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            updated,
            synchronize_session=False
        )
        self._session.commit()
