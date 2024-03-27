#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
# imports to use declarative_base of sqlachemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
# step 1: Create Base = declarative_base() before the class def below
Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    """Step 2: Add or replace in the class BaseModel:
    - id : column of string (60 chars), not null and primary key
    - created_at : column of datetime not null (default : curent datetime)
    - updated_at : column of datetime not null (default : curent datetime)
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at" or key == "updated_at":
                        setattr(self, key,
                                datetime.strptime(value,
                                                  "%Y-%m-%dT%H:%M:%S.%f"))
                    else:
                        setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Method to return a dictionary containing all keys/values"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary.keys():
            dictionary.pop('_sa_instance_state')
        return dictionary

    def delete(self):
        from models import storage
        storage.delete(self)
