#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = []


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


class KIC(Base):

    __tablename__ = "kic"

    id = Column(Integer, primary_key=True)
    kepler_id = Column(Integer)

    # Coordinates.
    ra = Column(Float)
    dec = Column(Float)

    # 2MASS.
    twomass_id = Column(Integer)
    twomass_name = Column(String)

    # Alternative reference.
    alt_id = Column(Integer)
    alt_ref = Column(Integer)

    # Star/Galaxy, etc.
    galaxy = Column(Boolean)
    variable = Column(Boolean)

    def __init__(self, kepler_id, ra, dec, twomass_id, twomass_name,
                 alt_id, alt_ref, galaxy, variable):
        kepler_id = kepler_id
        ra, dec = ra, dec
        twomass_id, twomass_name = twomass_id, twomass_name
        alt_id, alt_ref = alt_id, alt_ref
        galaxy, variable = galaxy, variable

    def __repr__(self):
        return ("<KIC({0.kepler_id}, {0.ra}, {0.dec}, {0.twomass_id}, "
                "'{0.twomass_name}', {0.alt_id}, {0.alt_ref}, "
                "{0.galaxy}, {0.variable})>").format(self)


class Reference(Base):

    __tablename__ = "literature"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    url = Column(String)
    arxiv_id = Column(String, unique=True)
    ref = Column(String)

    def __init__(self, name, url=None, arxiv_id=None, ref=None):
        self.name = name
        self.url = url
        self.arxiv_id = arxiv_id
        self.ref = ref

    def __repr__(self):
        return ("<Reference('{0.name}', url='{0.url}', "
                "arxiv_id='{0.arxiv_id}', ref='{0.ref}')>"
               ).format(self)


class MeasurementType(Base):

    __tablename__ = "measurement_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name, base_unit=None):
        self.name = name

    def __repr__(self):
        return "<MeasurementType('{0.name}')>".format(self)


class Measurement(Base):

    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True)

    obj_id = Column(Integer, ForeignKey("kic.id"))
    obj = relationship("KIC", backref=backref("measurements"))

    ref_id = Column(Integer, ForeignKey("literature.id"))
    ref = relationship("Reference", backref=backref("measurements"))

    measurement_type_id = Column(Integer, ForeignKey("measurement_types.id"))
    measurement_type = relationship("MeasurementType")

    unit = Column(String)

    # The value and error bars.
    value = Column(Float)
    uncert_plus = Column(Float)
    uncert_minus = Column(Float)

    def __init__(self, ref, measurement_type, unit, value, uncertainty=None):
        self.ref = ref
        self.measurement_type = measurement_type
        self.unit = unit
        self.value = value

        try:
            self.uncert_plus = uncertainty[0]
            self.uncert_minus = uncertainty[1]
        except (TypeError, ValueError, IndexError):
            self.uncert_plus = self.uncert_minus = uncertainty

    def __repr__(self):
        return ("<Measurement({0.ref}, {0.measurement_type}, {0.unit}, "
                "{0.value}, "
                "uncertainty=[{0.uncert_plus}, {0.uncert_minus}])>"
               ).format(self)
