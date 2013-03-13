#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)


import os
import kplr


_mt = kplr.models.MeasurementType
kic_mts = [
            _mt("pm_ra", "Proper motion in R.A."),
            _mt("pm_dec", "Proper motion in Dec."),
            _mt("umag", "SDSS u-band magnitude"),
            _mt("gmag", "SDSS g-band magnitude"),
            _mt("rmag", "SDSS r-band magnitude"),
            _mt("imag", "SDSS i-band magnitude"),
            _mt("zmag", "SDSS z-band magnitude"),
            _mt("gredmag", "Gred-band magnitude"),
            _mt("d51mag", "D51-band magnitude"),
            _mt("jmag", "2MASS J-band magnitude"),
            _mt("hmag", "2MASS H-band magnitude"),
            _mt("kmag", "2MASS K-band magnitude"),
            _mt("kepmag", "Kepler magnitude"),
            _mt("teff", "Effective temperature"),
            _mt("logg", "Log10 surface gravity (in cm/s/s)"),
            _mt("feh", "Log10 Fe/H metallicity"),
            _mt("ebv", "Excess B-V reddening"),
            _mt("av", "A-V extinction"),
            _mt("stellar_radius", "Stellar radius"),
            _mt("parallax", "Parallax"),
          ]


def _get(r, k, d):
    v = r.get(k, d)
    return v if r.get(k, "") != "" else d


def kic(kic_fn=None):
    # Database connection.
    session = kplr.Session()

    # Get the MAST reference.
    rt = kplr.models.Reference
    ref = session.query(rt).filter(rt.name == "MAST").all()
    ref = rt("MAST", doi="10.1088/0004-6256/142/4/112") if len(ref) == 0 \
                                                        else ref[0]

    # Build the measurement type list.
    mts = {}
    for m in kic_mts:
        mts[m.name] = session.query(kplr.models.MeasurementType).filter(
                        kplr.models.MeasurementType.name == m.name).all()[0]

    # Loop over the raw text KIC table.
    if kic_fn is None:
        kic_fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "raw", "kic.txt")

    with open(kic_fn) as f:
        for i, line in enumerate(f):
            if i == 0:
                # Get the field names from the first line.
                fields = [f.strip() for f in line.split("|")]
                continue

            # Parse the fields.
            kic = dict(zip(fields, line.split("|")))
            if i % 20 == 0:
                print(i, kic["kic_kepler_id"])

            # Parse the base object parameters.
            kic_obj = kplr.models.KIC(int(kic["kic_kepler_id"]),
                                      float(kic["kic_degree_ra"]),
                                      float(kic["kic_dec"]),
                                      int(_get(kic, "kic_tmid", -1)),
                                      kic.get("kic_tm_designation", None),
                                      int(_get(kic, "kic_altid", -1)),
                                      int(_get(kic, "kic_altsource", -1)),
                                      kic["kic_galaxy"] != "0",
                                      kic["kic_variable"] != "0",
                                      int(kic["kic_fov_flag"]))

            # Parse the measurements.
            for n, u, k, e in [
                            ("pm_ra", "arcsec/yr", "kic_pmra", None),
                            ("pm_dec", "arcsec/yr", "kic_pmdec", None),
                            ("umag", "mag", "kic_umag", None),
                            ("gmag", "mag", "kic_gmag", None),
                            ("rmag", "mag", "kic_rmag", None),
                            ("imag", "mag", "kic_imag", None),
                            ("zmag", "mag", "kic_zmag", None),
                            ("gredmag", "mag", "kic_gredmag", None),
                            ("d51mag", "mag", "kic_d51mag", None),
                            ("jmag", "mag", "kic_jmag", None),
                            ("hmag", "mag", "kic_hmag", None),
                            ("kmag", "mag", "kic_kmag", None),
                            ("teff", "K", "kic_teff", 200),
                            ("logg", None, "kic_logg", 0.5),
                            ("feh", None, "kic_feh", 0.5),
                            ("ebv", "mag", "kic_ebminusv", 0.1),
                            ("av", "mag", "kic_av", None),
                            ("stellar_radius", "R_sun", "kic_radius", None),
                            ("parallax", "arcsec", "kic_parallax", None),
                        ]:
                try:
                    measurement = kplr.models.KICMeasurement(ref, mts[n], u,
                                                             float(kic[k]),
                                                             uncertainty=e)

                except ValueError:
                    pass

                else:
                    kic_obj.measurements.append(measurement)

            # Save this object.
            session.add(kic_obj)
            session.commit()


if __name__ == "__main__":
    kplr.drop_all()
    kplr.create_all()

    session = kplr.Session()
    session.add_all(kic_mts)
    session.commit()

    kic()
