# -*- coding: utf-8 -*-

from __future__ import print_function
import pytest
from pytest import raises, approx

from datetime import date, datetime, timedelta, tzinfo
from rolex import util
from rolex.tz import utc, local


class EasternTime(tzinfo):
    """ET, Eastern Time, New York"""

    def utcoffset(self, dt):
        return timedelta(hours=-5)

    def tzname(self, dt):
        return "ET"

    def dst(self, dt):
        return timedelta(hours=-5)


et = EasternTime()


def test_to_ordinal():
    """
    Behave exactly same as date.toordinal()
    """
    a_date = date(2000, 1, 1)
    assert util.to_ordinal(a_date) == a_date.toordinal()


def test_from_ordinal():
    """
    Behave exactly same as date.fromordinal()
    """
    assert util.from_ordinal(730120) == date.fromordinal(730120)


def test_to_utctimestamp():
    # When datetime has tzinfo
    dt = datetime(1970, 1, 1, 0, 0, 1, tzinfo=utc)
    assert util.to_utctimestamp(dt) == 1

    dt = datetime(1969, 12, 31, 23, 59, 59, tzinfo=utc)
    assert util.to_utctimestamp(dt) == -1

    dt = datetime(1970, 1, 1, 0, 0, 0, tzinfo=et)
    assert util.to_utctimestamp(dt) == 18000

    # When datetime doens't have tzinfo
    dt = datetime(1970, 1, 1, 0, 0, 0)
    assert util.to_utctimestamp(dt) == 0


def test_from_utctimestamp():
    # Test if works as we expect
    assert util.from_utctimestamp(1) == datetime(1970, 1, 1, 0, 0, 1)
    assert util.from_utctimestamp(-1) == datetime(1969, 12, 31, 23, 59, 59)

    # See if works as same as datetime.utcfromtimestamp()
    timestamp = 1234567890
    assert util.from_utctimestamp(
        timestamp) == datetime.utcfromtimestamp(timestamp)

    # See if support negative timestamp
    timestamp = -1234567890
    a_datetime = util.from_utctimestamp(timestamp)
    assert a_datetime == datetime(1930, 11, 18, 0, 28, 30)


def test_to_utc():
    now_utc = datetime.utcnow()
    now_utc1 = util.to_utc(datetime.now(tz=local))
    now_utc2 = util.to_utc(datetime.utcnow())
    assert abs(now_utc1 - now_utc).total_seconds() < 1.0
    assert abs(now_utc2 - now_utc).total_seconds() < 1.0


def test_utc_to_tz():
    now_local = datetime.now()
    now_utc = datetime.utcnow()
    now_local1 = util.utc_to_tz(now_utc, local)
    now_local2 = util.utc_to_local(now_utc)
    assert abs(now_local1 - now_local).total_seconds() < 1.0
    assert abs(now_local2 - now_local).total_seconds() < 1.0


def test_is_weekend_weekday():
    d = date(2016, 5, 3)
    dt = datetime(2016, 5, 1, 8, 30)
    assert util.is_weekday(d) is True
    assert util.is_weekend(dt) is True


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
