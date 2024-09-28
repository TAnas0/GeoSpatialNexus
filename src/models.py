from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from .database import Base
from geoalchemy2 import Geometry
from sqlalchemy.orm import validates

from email_validator import (
    validate_email as validate_email_validator,
    EmailNotValidError,
)
import phonenumbers
import iso639
from forex_python.converter import CurrencyCodes
import json


CURRENCY_CODES = CurrencyCodes()


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String)
    language = Column(String)
    currency = Column(String)

    @validates("email")
    def validate_email(self, key, email):
        try:
            valid = validate_email_validator(email)
            return valid.email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {e}")

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        try:
            phone = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone):
                raise ValueError("Invalid phone number")
            return phonenumbers.format_number(
                phone, phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number format")

    @validates("language")
    def validate_language(self, key, language):
        if not iso639.languages.get(part1=language):
            raise ValueError("Invalid language code")
        return language

    @validates("currency")
    def validate_currency(self, key, currency):
        if not CURRENCY_CODES.get_symbol(currency):
            raise ValueError("Invalid currency code")
        return currency


class ServiceArea(Base):
    __tablename__ = "service_areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    geojson = Column(Geometry("POLYGON"), nullable=False)

    # Ensure price is positive at the database level
    __table_args__ = (CheckConstraint("price > 0", name="check_positive_price"),)

    @validates("price")
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be a positive value")
        return price

    @validates("geojson")
    def validate_geojson(self, key, geojson):
        try:
            # Parse and validate the GeoJSON structure
            from geoalchemy2.shape import to_shape
            geometry = to_shape(geojson)

            if geometry.geom_type != "Polygon":
                raise ValueError("GeoJSON must represent a POLYGON")

            return geojson
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(f"Invalid GeoJSON data: {e}")
