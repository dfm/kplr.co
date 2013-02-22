#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["Session"]


import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_URI = os.environ.get("KPLR_DB_URI", "postgresql+psycopg2:///kplr")
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)


from . import models


def drop_all():
    models.Base.metadata.drop_all(engine)


def create_all():
    models.Base.metadata.create_all(engine)
