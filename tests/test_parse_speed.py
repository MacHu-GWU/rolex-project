#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test how fast it can parse datetime.
"""

from __future__ import print_function
import time
from datetime import datetime

from rolex import rolex
from dateutil import parser


def bench_mark():
    """Test Result:
    
    - rolex is 4 ~ 5 times faster than dateutil.
    - rolex support more data type, can take string, timestamp, date or datetime
    
    Result::
    
        1 item, rolex takes 0.041573 sec, dateutil takes 0.000201 sec.
        10 item, rolex takes 0.000239 sec, dateutil takes 0.001051 sec.
        100 item, rolex takes 0.002138 sec, dateutil takes 0.009662 sec.
        1000 item, rolex takes 0.021126 sec, dateutil takes 0.097736 sec.
        10000 item, rolex takes 0.214618 sec, dateutil takes 0.977337 sec.
    """
    tpl = "%Y-%m-%dT%H:%M:%S"
     
    for n in [1, 10, 100, 1000, 10000]:
        data = [datetime.strftime(rolex.rnd_datetime(), tpl) for i in range(n)]
     
        st = time.clock()
        a = [rolex.parse_datetime(i) for i in data]
        elapse1 = time.clock() - st
         
        st = time.clock() 
        b = [parser.parse(i) for i in data]
        elapse2 = time.clock() - st
         
        print("%s item, rolex takes %.6f sec, dateutil takes %.6f sec." % (n, elapse1, elapse2))

        if n >= 10:
            assert elapse1 < elapse2


if __name__ == "__main__":
    bench_mark()