#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

import os
import kplr


_mt = kplr.models.MeasurementType
star_mts = {
            "teff": _mt("teff", "Effective temperature"),
            "logg": _mt("logg", "Log10 surface gravity (in cm/s/s)"),
            "feh": _mt("feh", "Log10 Fe/H metallicity"),
            "distance": _mt("distance", "Distance"),
            "radius": _mt("stellar_radius", "Stellar radius"),
            "mass": _mt("stellar_mass", "Stellar mass"),
           }


def stars(fn="raw/dressing_stars.txt"):
    with open(fn) as f:
        for i, line in enumerate(f):
            if i >= 28:
                pass


if __name__ == "__main__":
    session = kplr.Session()

    # FIXME
    for k, m in star_mts.iteritems():
        mt = session.query(kplr.models.MeasurementType).filter(
                        kplr.models.MeasurementType.name == m.name).all()

        if mt is None or len(mt) == 0:
            session.add(m)

        star_mts[m.name] =

    session.commit()

    kic()
