# -*- coding: utf-8 -*-

"""
Limitation of standard datetime library.

**中文文档**

- 在Python27中, datetime类没有实现 ``datetime.timestamp()`` 方法
- 在Python3中, 对于1970年之前的时间无法获得timestamp
- 在Python3中, datetime.fromtimestamp(timestamp) 不支持负值
"""

from __future__ import print_function
from datetime import datetime, date


def datetime_timestamp_method_not_implemented_in_python2():
    try:
        dt = datetime(2014, 1, 1)
        print(dt.timestamp())
    except Exception as e:
        print("datetime.timestamp() is not implemented in Python2; %s" % e)


def datetime_timestamp_not_support_datetime_before_1970_01_01_in_python3():
    try:
        dt = datetime(1900, 1, 1)
        print(dt.timestamp())
    except Exception as e:
        print(
            "datetime.timestamp() doesn't support datetime before 1970-01-01; %s" % e)


def datetime_fromtimestamp_not_support_negative_value():
    try:
        dt = datetime.fromtimestamp(-1)
        print(dt)
    except Exception as e:
        print("datetime.fromtimestamp() doesn't support negative value; %s" % e)


if __name__ == "__main__":
    datetime_timestamp_method_not_implemented_in_python2()
    datetime_timestamp_not_support_datetime_before_1970_01_01_in_python3()
    datetime_fromtimestamp_not_support_negative_value()
