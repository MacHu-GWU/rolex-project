#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Limitation of standard datetime library.
"""

from __future__ import print_function
from datetime import datetime, date

# datetime.timestamp() is not implemented in Python2
try:
    dt = datetime(2014, 1, 1)
    print(dt.timestamp())
except Exception as e:
    print("datetime.timestamp() is not implemented in Python2")

# datetime.timestamp() doesn't support datetime before 1970-01-01
try:
    dt = datetime(1900, 1, 1)
    print(dt.timestamp())
except Exception as e:
    print("datetime.timestamp() doesn't support datetime before 1970-01-01")

# datetime.fromtimestamp() doesn't support negative value
try:
    dt = datetime.fromtimestamp(-1)
    print(dt)
except Exception as e:
    print("datetime.fromtimestamp() doesn't support negative value")