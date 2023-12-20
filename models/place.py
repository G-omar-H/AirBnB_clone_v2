#!/usr/bin/python3
""" Place Module for HBNB project """
from tempfile import gettempprefix
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Float, String, ForeignKey, Column, Table
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

        reviews_list = []
        for k, v in storage.all():
            if k.partition(".")[0] == "Review":
                if v.place_id == self.id:
                    reviews_list.append(v)
        return reviews_list

    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column("place_id", String(60),
               ForeignKey("places.id"),
               primary_key=True),
        Column("amenity_id", String(60),
               ForeignKey("amenities.id"),
               primary_key=True),
    )

    amenities = relationship(
        "Amenity", backref="place_amenities",
        secondary="place_amenity", viewonly=False
    )

    @property
    def get_amenities(self):
        """
        Getter attribute amenities that returns the list of Amenity instances
        based on the attribute amenity_ids
        that contains all Amenity.id linked to the Place
        """
        from models import storage

        amenins = []
        for k, v in storage.all():
            if k.partition(".")[0] == "Amenity":
                if v.id in self.amenity_ids:
                    amenins.append(v)
        return amenins

    def set_amenity_ids(self, obj):
        """
        Setter attribute amenities that handles append method
        for adding an Amenity.id to the attribute amenity_ids.
        This method should accept only Amenity object, otherwise,
        do nothing.
        """
        if obj.__class__.__name__ == "Amenity":
            self.amenity_ids.append(obj.id)
