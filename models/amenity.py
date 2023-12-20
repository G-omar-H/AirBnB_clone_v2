#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Float, String, Column, ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)

    place_amenities = relationship(
        "Place", back_populates="amenities", secondary="place_amenity"
    )
