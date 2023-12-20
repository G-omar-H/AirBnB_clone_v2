#!/usr/bin/python3
""" Place Module for HBNB project """
from tempfile import gettempprefix
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Float, String, Column, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """A place to stay"""

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(128), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    user = relationship("User", back_populates="places")
    cities = relationship("City", back_populates="places")
    reviews = relationship(
        "Review", back_populates="place", cascade="all, delete-orphan"
    )

    @property
    def get_reviews(self):
        """
        Getter attribute reviews that returns the list of Review instances
        with place_id equals
        to the current Place.id => It will be the FileStorage
        relationship between Place and Review
        """
        from models import storage

        for k, v in storage.all():
            if k.partition(".")[0] == "Review":
                return [i for i in v if v.place_id == self.id]
