#!/usr/bin/python3
"""This module defines a class State"""
import models
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """Defines new attributes for the State class"""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="delete", backref="state")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Method that returns a list of City instances with state_id"""
            cities_list = []
            for city_obj in models.storage.all(City).values():
                if self.id == city_obj.state_id:
                    cities_list.append(city_obj)
            return cities_list
