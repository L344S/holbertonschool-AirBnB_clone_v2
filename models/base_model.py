#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
# imports to use declarative_base of sqlachemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# step 1: Create Base = declarative_base() before the class def below
Base = declarative_base()

# exemple de la documentation :
"""
class SomeClass(Base):
    __tablename__ = 'some_table'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))
https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html
https://docs.sqlalchemy.org/en/20/core/constraints.html
"""


class BaseModel:
    """A base class for all hbnb models"""
    """Step 2: Add or replace in the class BaseModel:
    - id : column of string (60 chars), not null and primary key
    - created_at : column of datetime not null (default : curent datetime)
    - updated_at : column of datetime not null (default : curent datetime)
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(datetime, nullable=False, default=datetime.now())
    updated_at = Column(datetime, nullable=False, default=datetime.now())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            for key, value in kwargs.items():
                # self.__dict__[key]= value
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
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop("_sa_instance_state")
        return dictionary

    def delete(self):
        from models import storage
        storage.delete(self)
