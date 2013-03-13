#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["KIC"]


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


class KIC(Base):
    """
    The entry for a star from the Kepler Input Catalog (KIC). The measured
    values from the input catalog are stored with the reference "MAST" in the
    ``measurements`` relationship.

    :param kepler_id: (Integer)
        The ID of the star in the KIC.

    :param ra: (Float)
        The R.A. of the star in degrees.

    :param dec: (Float)
        The Dec. of the star in degrees.

    :param twomass_id: (Integer)
        The ID from the 2MASS catalog or ``None``.

    :param twomass_name: (String)
        The name of the star from the KIC.

    :param alt_id: (Integer)
        The ID of the star from another catalog (referenced by the
        ``alt_ref`` property.

    :param alt_ref: (Integer)
        The reference catalog for the alternate ID.
            - 0: null
            - 1: Hipparcos catalog
            - 2: Tycho2
            - 3: UCAC2
            - 4: General Catalog of Var. Stars
            - 5: Lepine proper motion catalog star
            - 11: NED
            - 12: Extended 2MASS
            - 13: FIRST
            - 14: NVSS catalog
            - 15: VLBA catalog
            - 16: CHANDRA catalog

    :param galaxy: (Boolean)
        Is this actually a galaxy?

    :param variable: (Boolean)
        Is the source variable?

    """

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
    fov_flag = Column(Integer)

    def __init__(self, kepler_id, ra, dec, twomass_id, twomass_name,
                 alt_id, alt_ref, galaxy, variable, fov_flag):
        self.kepler_id = int(kepler_id)
        self.ra, self.dec = float(ra), float(dec)
        self.twomass_id, self.twomass_name = \
                                    int(twomass_id), unicode(twomass_name)
        self.alt_id, self.alt_ref = int(alt_id), int(alt_ref)
        self.galaxy, self.variable = bool(galaxy), bool(variable)
        self.fov_flag = int(fov_flag)

    def __repr__(self):
        return ("<KIC({0.kepler_id}, {0.ra}, {0.dec}, {0.twomass_id}, "
                "'{0.twomass_name}', {0.alt_id}, {0.alt_ref}, "
                "{0.galaxy}, {0.variable}, {0.fov_flag})>").format(self)


class KICMeasurement(Base):

    __tablename__ = "kic_measurements"

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


class MeasurementType(Base):

    __tablename__ = "measurement_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<MeasurementType('{0.name}', '{0.description}')>".format(self)


class Reference(Base):

    __tablename__ = "literature"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    url = Column(String)
    doi = Column(String, unique=True)
    arxiv_id = Column(String, unique=True)

    def __init__(self, name, url=None, doi=None, arxiv_id=None):
        self.name = name
        self.url = url
        self.doi = doi
        self.arxiv_id = arxiv_id

    def __repr__(self):
        return ("<Reference('{0.name}', url='{0.url}', "
                "arxiv_id='{0.arxiv_id}', doi='{0.doi}')>"
               ).format(self)
