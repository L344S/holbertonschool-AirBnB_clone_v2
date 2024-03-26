#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, Integer, String
from models.engine import db_storage
from sqlalchemy.orm import relationship


class State(BaseModel):
    
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")

@property
def cities(self):
    from models import storage
    from models import city
    city_list = []
    for key, value in storage.all(city).items():
        if value.state_id == self.id:
            city_list.append(value)
    return city_list
