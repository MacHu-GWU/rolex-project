# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from rolex import math
from datetime import datetime


def test_add_seconds_minutes_hours_days_weeks():
    assert math.add_seconds("2014-01-01", 1) == datetime(2014, 1, 1, 0, 0, 1)
    assert math.add_minutes("2014-01-01", 1) == datetime(2014, 1, 1, 0, 1, 0)
    assert math.add_hours("2014-01-01", 1) == datetime(2014, 1, 1, 1, 0, 0)
    assert math.add_days("2014-01-01 18:30:25", 1) == \
        datetime(2014, 1, 2, 18, 30, 25)
    assert math.add_weeks("2014-01-01 18:30:25", 1) == \
        datetime(2014, 1, 8, 18, 30, 25)


def test_add_months():
    assert math.add_months("2012-01-31", 1) == datetime(2012, 2, 29)
    assert math.add_months("2012-03-31", -1) == datetime(2012, 2, 29)

    assert math.add_months("2012-03-31", -13) == datetime(2011, 2, 28)
    assert math.add_months("2012-03-31", 11) == datetime(2013, 2, 28)

    assert math.add_months("2012-12-31", 1) == datetime(2013, 1, 31)
    assert math.add_months("2012-12-31", 2) == datetime(2013, 2, 28)
    assert math.add_months("2012-12-31", 3) == datetime(2013, 3, 31)
    assert math.add_months("2012-12-31", 4) == datetime(2013, 4, 30)


def test_add_years():
    assert math.add_years("2012-02-29", 1) == datetime(2013, 2, 28)
    assert math.add_years("2012-02-29", -1) == datetime(2011, 2, 28)

    assert math.add_years("2011-02-28", 1) == datetime(2012, 2, 28)
    assert math.add_years("2013-02-28", -1) == datetime(2012, 2, 28)


def test_round_to():
    dt = datetime(2000, 4, 15, 10, 0, 0)

    assert math.round_to(dt, 9, 0, 0, mode="floor") == \
        datetime(2000, 4, 15, 9, 0, 0)
    assert math.round_to(dt, 11, 0, 0, mode="floor") == \
        datetime(2000, 4, 14, 11, 0, 0)

    assert math.round_to(dt, 11, 0, 0, mode="ceiling") == \
        datetime(2000, 4, 15, 11, 0, 0)
    assert math.round_to(dt, 9, 0, 0, mode="ceiling") == \
        datetime(2000, 4, 16, 9, 0, 0)

    assert math.round_to(dt, 9, 0, 0, mode="round") == \
        datetime(2000, 4, 15, 9, 0, 0)
    assert math.round_to(dt, 11, 0, 0, mode="round") == \
        datetime(2000, 4, 15, 11, 0, 0)
    assert math.round_to(dt, 10, 0, 0, mode="round") == \
        datetime(2000, 4, 15, 10, 0, 0)

    assert math.round_to(dt, 22, 0, 0, mode="round") == \
        datetime(2000, 4, 14, 22, 0, 0)

    with raises(ValueError):
        math.round_to(dt, 8, 0, 0, mode="Unknown")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
