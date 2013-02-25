#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)


import kplr
import requests


base_url = "http://archive.stsci.edu/kepler/{0}/search.php"


def mast_request(category, **params):
    """
    Submit a request to the API and return the JSON response.

    :param category:
        The table that you want to search.

    :param **kwargs:
        Any other search parameters.

    """
    params["action"] = params.get("action", "Search")
    params["outputformat"] = "JSON"
    params["verb"] = 3
    params["coordformat"] = "dec"
    r = requests.get(base_url.format(category), params=params)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    try:
        return r.json()
    except ValueError:
        return None


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


def kic():
    # Database connection.
    session = kplr.Session()
    i = 0
    while 1:
        i += 1
        r = mast_request("kic10", kic_kepler_id=i, max_records=1)[0]
        print(r["Kepler ID"])
        # Build the KIC object.
        kic_obj = kplr.models.KIC(int(r["Kepler ID"]),
                            float(r["RA (J2000)"]), float(r["Dec (J2000)"]),
                            int(_get(r, "2MASS Designation", -1)),
                            r.get("2MASS ID", None),
                            int(_get(r, "Alt ID", -1)),
                            int(_get(r, "Alt ID Source", -1)),
                            r["Star/Gal ID"] == "1", r["Var. ID"] == "1")

        # Get the MAST reference.
        rt = kplr.models.Reference
        ref = session.query(rt).filter(rt.name == "MAST").all()
        ref = rt("MAST") if len(ref) == 0 else ref[0]

        # Parse the measurements.
        for n, u, k, e in [
                        ("pm_ra", "arcsec/yr", "RA PM (arcsec/yr)", None),
                        ("pm_dec", "arcsec/yr", "Dec PM (arcsec/yr)", None),
                        ("umag", "mag", "u Mag", None),
                        ("gmag", "mag", "g Mag", None),
                        ("rmag", "mag", "r Mag", None),
                        ("imag", "mag", "i Mag", None),
                        ("zmag", "mag", "z Mag", None),
                        ("gredmag", "mag", "Gred Mag", None),
                        ("d51mag", "mag", "D51 Mag", None),
                        ("jmag", "mag", "J Mag", None),
                        ("hmag", "mag", "H Mag", None),
                        ("kmag", "mag", "K Mag", None),
                        ("teff", "K", "Teff (deg K)", 200),
                        ("logg", None, "Log G (cm/s/s)", 0.5),
                        ("feh", None, "Metallicity (solar=0.0)", 0.5),
                        ("ebv", "mag", "E(B-V)", 0.1),
                        ("av", "mag", "A_V", None),
                        ("stellar_radius", "R_sun", "Radius (solar=1.0)",
                                                                        None),
                        ("parallax", "arcsec", "Parallax (arcsec)", None),
                        ]:

            t = session.query(kplr.models.MeasurementType).filter(
                                kplr.models.MeasurementType.name == n).all()[0]

            # Save the measurement.
            try:
                kic_obj.measurements.append(
                            kplr.models.KICMeasurement(ref, t, u, float(r[k]),
                                                    uncertainty=e)
                        )
            except ValueError:
                pass

        session.add(kic_obj)
        session.commit()


if __name__ == "__main__":
    kplr.drop_all()
    kplr.create_all()

    session = kplr.Session()
    session.add_all(kic_mts)
    session.commit()

    kic()
