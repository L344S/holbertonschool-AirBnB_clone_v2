#!/usr/bin/python3
"""This module define a class DBSstorage"""
import json
import models
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import MetaData
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State

import os

MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
MYSQL_DB = os.getenv('HBNB_MYSQL_DB')

"""
from sqlalchemy import create_engine

# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'password'
host = '127.0.0.1'
port = 3306
database = 'GeeksForGeeks'

# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, MYSQL_DB
        )
    )

"""


class DBStorage:
    """New engine DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """init method to create a new instance of DBStorage"""

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_DB), pool_pre_ping=True)
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        dictionary = {}
        classes = [User, State, City, Amenity, Place, Review]
        if not cls:
            for x in classes:
                for obj in self.__session.query(x).all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    dictionary[key] = obj
        else:
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                dictionary[key] = obj
        return dictionary

    def new(self, obj):
        """Method to add the object to the current database session"""
        if obj:
            self.__session.add(obj)
    
    def save(self):
        """Method to commit all changes of the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Method to delete obj from the current db session if not None"""
        if obj:
            self.__session.delete()
            self.save()

    def reload(self):
        """Create all tables and the current database session"""
        Base.metadata.create_all(self.__engine)
        session_create = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_create)
        self.__session = Session()
