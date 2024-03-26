#!/usr/bin/python3
"""This module define a class DBSstorage"""
import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """New engine DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """init method to create a new instance of DBStorage"""
        MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
        MYSQL_ENV = os.getenv("HBNB_ENV")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_DB),
            pool_pre_ping=True)
        if MYSQL_ENV == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        dictionary = {}
        classes = [User, State, City, Amenity, Place, Review]

        if not cls:
            for x in classes:
                for obj in self.__session.query(x).all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    dictionary[key] = obj
        else:
            if isinstance(cls, str):
                cls = classes.get(cls, None)
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
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and the current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
