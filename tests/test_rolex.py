#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
rolex.__init__.py unittest
"""

import pytest
import sys
import unittest

from datetime import datetime, date, timedelta, tzinfo
from rolex import rolex, utc
from rolex.six import PY3


class ET(tzinfo):
    """ET, Eastern Time, New York"""

    def utcoffset(self, dt):
        return timedelta(hours=-5)

    def tzname(self, dt):
        return "ET"

    def dst(self, dt):
        return timedelta(hours=-5)

et = ET()


def test_str2date():
    assert rolex.str2date("9/21/2014") == date(2014, 9, 21)
    assert rolex.default_date_template == "%m/%d/%Y"


def test_str2datetime():
    assert rolex.str2datetime(
        "2014-07-13 8:12:34 PM") == datetime(2014, 7, 13, 20, 12, 34)
    assert rolex.default_datetime_template == "%Y-%m-%d %I:%M:%S %p"
    assert rolex.str2datetime.__name__ == "_str2datetime"
    
    # When rolex failed to parse date time string, 
    # then start using dateutil.parser.parse
    assert isinstance(rolex.str2datetime("2000-01-01T00:00:00-5"), datetime)
    assert rolex.str2datetime.__name__ == "parse"
    

def test_parse_date():
    """parse anything to date.
    """
    assert rolex.parse_date("10-1-1949") == date(1949, 10, 1)
    assert rolex.parse_date(711766) == date(1949, 10, 1)
    assert rolex.parse_date(
        datetime(1949, 10, 1, 8, 15, 0)) == date(1949, 10, 1)


def test_parse_datetime():
    """parse anything to datetime.
    """
    assert rolex.parse_datetime(
        "1949-10-1 8:15:00") == datetime(1949, 10, 1, 8, 15)
    assert rolex.parse_datetime(-1.0) == datetime(1969, 12, 31, 23, 59, 59)
    assert rolex.parse_datetime(1.0) == datetime(1970, 1, 1, 0, 0, 1)
    assert rolex.parse_datetime(
        datetime(1949, 10, 1, 8, 30, 0)) == datetime(1949, 10, 1, 8, 30, 0)
    assert rolex.parse_datetime(date(1949, 10, 1)) == datetime(1949, 10, 1)


def test_toordinal_fromordinal():
    # 是否和date.toordinal()的结果一致
    d = date(2014, 9, 21)
    assert rolex.to_ordinal(d) == d.toordinal()

    # 是否和date.fromordinal(int)的结果一致
    assert rolex.from_ordinal(701135) == date.fromordinal(701135)


def test_to_utctimestamp():
    # When datetime has tzinfo
    dt = datetime(1970, 1, 1, 0, 0, 1, tzinfo=utc)
    assert rolex.to_utctimestamp(dt) == 1

    dt = datetime(1969, 12, 31, 23, 59, 59, tzinfo=utc)
    assert rolex.to_utctimestamp(dt) == -1

    dt = datetime(1970, 1, 1, 0, 0, 0, tzinfo=et)
    assert rolex.to_utctimestamp(dt) == 18000

    # When datetime doens't have tzinfo
    dt = datetime(1970, 1, 1, 0, 0, 0)
    assert rolex.to_utctimestamp(dt) == 0


def test_from_utctimestamp():
    # Test if works as we expect
    assert rolex.from_utctimestamp(1) == datetime(1970, 1, 1, 0, 0, 1)
    assert rolex.from_utctimestamp(-1) == datetime(1969, 12, 31, 23, 59, 59)

    # See if works as same as datetime.utcfromtimestamp()
    timestamp = 1234567890
    assert rolex.from_utctimestamp(
        timestamp) == datetime.utcfromtimestamp(timestamp)

    # See if support negative timestamp
    timestamp = -1234567890
    rolex.from_utctimestamp(timestamp)


def test_to_timestamp():
    # Because only Py3 datetime object has to_timestamp() method.
    if PY3:
        dt = datetime(1970, 1, 1, 0, 0, 0, tzinfo=utc)
        assert rolex.to_timestamp(dt) == 0

        # This datetime would be considered as a local time
        dt = datetime(1970, 1, 1, 0, 0, 1)
        assert rolex.to_timestamp(dt) == dt.timestamp()


def test_from_timestamp():
    dt = rolex.from_timestamp(-3600)
    assert rolex.from_timestamp(1) == datetime.fromtimestamp(1)


def test_time_series():
    """Test time_series generator method.
    """
    # test start + end
    assert rolex.time_series(
        start="2014-01-01 03:00:00",
        end="2014-01-01 03:10:00",
        freq="5min",
    ) == [
        datetime(2014, 1, 1, 3, 0, 0),
        datetime(2014, 1, 1, 3, 5, 0),
        datetime(2014, 1, 1, 3, 10, 0),
    ]

    # test start + periods
    assert rolex.time_series(
        start="2014-01-01 03:00:00",
        periods=3,
        freq="5min",
    ) == [
        datetime(2014, 1, 1, 3, 0, 0),
        datetime(2014, 1, 1, 3, 5, 0),
        datetime(2014, 1, 1, 3, 10, 0),
    ]

    # test end + periods
    assert rolex.time_series(
        end="2014-01-01 03:10:00",
        periods=3,
        freq="5min",
    ) == [
        datetime(2014, 1, 1, 3, 0, 0),
        datetime(2014, 1, 1, 3, 5, 0),
        datetime(2014, 1, 1, 3, 10, 0),
    ]

    # test take datetime as input
    assert rolex.time_series(
        start=datetime(2014, 1, 1, 3, 0, 0),
        end=datetime(2014, 1, 1, 3, 10, 0),
        freq="5min",
    ) == [
        datetime(2014, 1, 1, 3, 0, 0),
        datetime(2014, 1, 1, 3, 5, 0),
        datetime(2014, 1, 1, 3, 10, 0),
    ]


def test_weekday_series():
    assert rolex.weekday_series(
        "2014-01-01 06:30:25",
        "2014-02-01 06:30:25",
        weekday=2,
    ) == [
        datetime(2014, 1, 7, 6, 30, 25),
        datetime(2014, 1, 14, 6, 30, 25),
        datetime(2014, 1, 21, 6, 30, 25),
        datetime(2014, 1, 28, 6, 30, 25),
    ]


def test_is_weekend_weekday():
    """Test isweekday and isweekend checker method.
    """
    d = date(2016, 5, 3)
    dt = datetime(2016, 5, 1, 8, 30)
    assert rolex.isweekday(d) is True
    assert rolex.isweekend(dt) is True


def test_rnd_date():
    # test random date is between the boundary
    d = rolex.rnd_date("2014-01-01", date(2014, 1, 31))
    assert d >= date(2014, 1, 1)
    assert d <= date(2014, 1, 31)

    d = rolex.rnd_date("2014-06-01", "2014-06-01")
    assert d == date(2014, 6, 1)


def test_rnd_date_array():
    start, end = "2014-01-01", date(2014, 1, 31)
    array = rolex.rnd_date_array(4, start, end)
    assert len(array) == 4

    matrix = rolex.rnd_date_array((2, 3), start, end)
    assert len(matrix) == 2
    assert len(matrix[0]) == 3


def test_rnd_datetime():
    # test random datetime is between the boundary
    dt = rolex.rnd_datetime("2014-01-01", datetime(2014, 1, 31, 23, 59, 59))
    assert dt >= datetime(2014, 1, 1, 0, 0, 0)
    assert dt <= datetime(2014, 1, 31, 23, 59, 59)

    dt = rolex.rnd_datetime("2014-06-01 6:30:00", "2014-06-01 6:30:00")
    assert dt == datetime(2014, 6, 1, 6, 30)


def test_rnd_datetime_array():
    start, end = "2014-01-01", datetime(2014, 1, 31, 23, 59, 59)
    array = rolex.rnd_datetime_array(4, start, end)
    assert len(array) == 4

    matrix = rolex.rnd_datetime_array((2, 3), start, end)
    assert len(matrix) == 2
    assert len(matrix[0]) == 3


def test_add_seconds_minutes_hours():
    assert rolex.add_seconds("2014-01-01", 1) == datetime(2014, 1, 1, 0, 0, 1)
    assert rolex.add_minutes("2014-01-01", 1) == datetime(2014, 1, 1, 0, 1, 0)
    assert rolex.add_hours("2014-01-01", 1) == datetime(2014, 1, 1, 1, 0, 0)
    assert rolex.add_days("2014-01-01 18:30:25",
                          1) == datetime(2014, 1, 2, 18, 30, 25)


def test_add_months():
    assert rolex.add_months("2012-03-31", -1) == datetime(2012, 2, 29)
    assert rolex.add_months("2012-03-30", -13) == datetime(2011, 2, 28)
    assert rolex.add_months("2012-03-29", 11) == datetime(2013, 2, 28)
    assert rolex.add_months("2012-06-30", 1) == datetime(2012, 7, 30)


def test_add_years():
    assert rolex.add_years("2012-02-29", -1) == datetime(2011, 2, 28)
    assert rolex.add_years("2012-02-29", -1) == datetime(2011, 2, 28)
    assert rolex.add_years("2012-02-29", -1) == datetime(2011, 2, 28)

    assert rolex.add_years("2011-02-28", 1) == datetime(2012, 2, 28)


def test_day_month_year_interval():
    start, end = rolex.day_interval(2014, 3, 5, return_string=True)
    assert (start, end) == ("2014-03-05 00:00:00", "2014-03-05 23:59:59")

    start, end = rolex.day_interval(2014, 12, 31, return_string=False)
    assert (start, end) == (datetime(2014, 12, 31, 0, 0, 0),
                            datetime(2014, 12, 31, 23, 59, 59))

    start, end = rolex.month_interval(2014, 3, return_string=True)
    assert (start, end) == ("2014-03-01 00:00:00", "2014-03-31 23:59:59")

    start, end = rolex.month_interval(2014, 12, return_string=False)
    assert (start, end) == (datetime(2014, 12, 1, 0, 0, 0),
                            datetime(2014, 12, 31, 23, 59, 59))

    start, end = rolex.year_interval(2014, return_string=True)
    assert (start, end) == ("2014-01-01 00:00:00", "2014-12-31 23:59:59")

    start, end = rolex.year_interval(2014, return_string=False)
    assert (start, end) == (datetime(2014, 1, 1, 0, 0, 0),
                            datetime(2014, 12, 31, 23, 59, 59))


def test_round_to_specified_time():
    assert rolex.round_to(
        datetime(2014, 6, 1, 0, 0, 0),
        hour=0, minute=0, second=0, mode="floor"
    ) == datetime(2014, 6, 1)

    assert rolex.round_to(
        datetime(2014, 6, 1, 23, 59, 59),
        hour=0, minute=0, second=0, mode="floor"
    ) == datetime(2014, 6, 1)

    assert rolex.round_to(
        datetime(2014, 6, 1, 0, 0, 0),
        hour=0, minute=0, second=0, mode="ceiling"
    ) == datetime(2014, 6, 1)

    assert rolex.round_to(
        datetime(2014, 6, 1, 23, 59, 59),
        hour=0, minute=0, second=0, mode="ceiling"
    ) == datetime(2014, 6, 2)


if __name__ == "__main__":
    import py
    import os
    py.test.cmdline.main("%s --tb=native -s" % os.path.basename(__file__))