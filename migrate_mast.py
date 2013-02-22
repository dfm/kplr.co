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
    r = requests.get(base_url.format(category), params=params)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    try:
        return r.json()
    except ValueError:
        return None


def kic():
    r = mast_request("kic10", max_records=1)

    session = kplr.Session()

    # Get the MAST reference.
    rt = kplr.models.Reference
    ref = session.query(rt).filter(rt.name == "MAST").all()
    if len(ref) == 0:
        ref = rt("MAST")
    else:
        ref = ref[0]

    # Parse the measurements.
    measurements = []
    mt = kplr.models.MeasurementType
    for n, u, k in [
                    ("umag", "mag", "u Mag"),
                    ("gmag", "mag", "g Mag"),
                    ("rmag", "mag", "r Mag"),
                    ("imag", "mag", "i Mag"),
                    ("zmag", "mag", "z Mag"),
                   ]:

        # Upsert the measurement type reference.
        res = session.query(mt).filter(mt.name == n).all()
        if len(res) == 0:
            t = mt(n)
        else:
            t = res[0]

        # Save the measurement.
        try:
            measurements.append(
                        kplr.models.Measurement(ref, t, u, float(r[0][k]))
                    )
        except ValueError:
            pass

    print(measurements)

    session.add_all(measurements)
    session.commit()


if __name__ == "__main__":
    # kplr.drop_all()
    # kplr.create_all()
    kic()
