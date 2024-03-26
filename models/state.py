#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os

sto = os.getenv("HBNB_TYPE_STORAGE")


class State(BaseModel):
    """ State class """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if sto == 'db':
        cities = relationship("City", back_populates="state", cascade="all",
                              passive_deletes=True)
    else:
        @property
        def cities(self):
            """commentaire qu'il manque"""
            from models import storage
            from models import City
            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
