# -*- coding: utf-8 -*-

import time
import pytest
from pytest import raises
from rolex import generator
from datetime import datetime, date


def test_time_series():
    """Test time_series generator method.
    """
    # test start + end
    assert generator.time_series(
        start="2014-01-01 03:00:00",
        end="2014-01-01 03:10:00",
        freq="5min",
    ) == \
        [
        datetime(2014, 1, 1, 3, 0, 0),
        datetime(2014, 1, 1, 3, 5, 0),
        datetime(2014, 1, 1, 3, 10, 0),
    ]

    # test start + periods
    assert generator.time_series(
        start="2014-01-01 03:00:00",
        periods=3,
        freq="5min",
    ) == \
        [
        datetime(2014, 1, 1, 3, 0, 0),
        datetime(2014, 1, 1, 3, 5, 0),
        datetime(2014, 1, 1, 3, 10, 0),
    ]

    # test end + periods
    assert generator.time_series(
        end="2014-01-01 03:10:00",
        periods=3,
        freq="5min",
    ) == \
        [
        datetime(2014, 1, 1, 3, 0, 0),
        datetime(2014, 1, 1, 3, 5, 0),
        datetime(2014, 1, 1, 3, 10, 0),
    ]

    # test take datetime as input
    assert generator.time_series(
        start=datetime(2014, 1, 1, 0, 0, 0),
        end=datetime(2014, 1, 3, 23, 59, 59),
        freq="25hour",
        normalize=True,
    ) == \
        [
        datetime(2014, 1, 1),
        datetime(2014, 1, 2),
        datetime(2014, 1, 3),
    ]

    with raises(Exception):
        generator.time_series()


def test_weekday_series():
    assert generator.weekday_series(
        "2014-01-01 06:30:25",
        "2014-02-01 06:30:25",
        weekday=2,
    ) == \
        [
        datetime(2014, 1, 7, 6, 30, 25),
        datetime(2014, 1, 14, 6, 30, 25),
        datetime(2014, 1, 21, 6, 30, 25),
        datetime(2014, 1, 28, 6, 30, 25),
    ]


def test_rnd_date():
    # test random date is between the boundary
    d = generator.rnd_date("2014-01-01", date(2014, 1, 31))
    assert d >= date(2014, 1, 1)
    assert d <= date(2014, 1, 31)

    d = generator.rnd_date("2014-06-01", "2014-06-01")
    assert d == date(2014, 6, 1)


def test_rnd_date_array():
    start, end = "2014-01-01", date(2014, 1, 31)
    array = generator.rnd_date_array(4, start, end)
    assert len(array) == 4

    matrix = generator.rnd_date_array((2, 3), start, end)
    assert len(matrix) == 2
    assert len(matrix[0]) == 3


def test_rnd_datetime():
    # test random datetime is between the boundary
    dt = generator.rnd_datetime(
        "2014-01-01", datetime(2014, 1, 31, 23, 59, 59))
    assert dt >= datetime(2014, 1, 1, 0, 0, 0)
    assert dt <= datetime(2014, 1, 31, 23, 59, 59)

    dt = generator.rnd_datetime("2014-06-01 6:30:00", "2014-06-01 6:30:00")
    assert dt == datetime(2014, 6, 1, 6, 30)


def test_rnd_datetime_array():
    start, end = "2014-01-01", datetime(2014, 1, 31, 23, 59, 59)
    array = generator.rnd_datetime_array(4, start, end)
    assert len(array) == 4

    matrix = generator.rnd_datetime_array((2, 3), start, end)
    assert len(matrix) == 2
    assert len(matrix[0]) == 3


def test_rnd_():
    size = 10000

    st = time.clock()
    generator.rnd_date_array(size)
    elapse1 = time.clock() - st

    st = time.clock()
    generator.rnd_date_list_high_performance(size)
    elapse2 = time.clock() - st

    # assert elapse2 < elapse1

    st = time.clock()
    generator.rnd_datetime_array(size)
    elapse1 = time.clock() - st

    st = time.clock()
    generator.rnd_datetime_list_high_performance(size)
    elapse2 = time.clock() - st

    assert elapse2 < elapse1


def test_day_month_year_interval():
    start, end = generator.day_interval(2014, 3, 5, return_string=True)
    assert (start, end) == ("2014-03-05 00:00:00", "2014-03-05 23:59:59")

    start, end = generator.day_interval(2014, 12, 31, return_string=False)
    assert (start, end) == (datetime(2014, 12, 31, 0, 0, 0),
                            datetime(2014, 12, 31, 23, 59, 59))

    start, end = generator.month_interval(2014, 3, return_string=True)
    assert (start, end) == ("2014-03-01 00:00:00", "2014-03-31 23:59:59")

    start, end = generator.month_interval(2014, 12, return_string=False)
    assert (start, end) == (datetime(2014, 12, 1, 0, 0, 0),
                            datetime(2014, 12, 31, 23, 59, 59))

    start, end = generator.year_interval(2014, return_string=True)
    assert (start, end) == ("2014-01-01 00:00:00", "2014-12-31 23:59:59")

    start, end = generator.year_interval(2014, return_string=False)
    assert (start, end) == (datetime(2014, 1, 1, 0, 0, 0),
                            datetime(2014, 12, 31, 23, 59, 59))

    with raises(Exception):
        generator._randn(-1, generator.rnd_datetime)

    with raises(Exception):
        generator._randn((-1, -1), generator.rnd_datetime)

    with raises(Exception):
        generator._randn("12", generator.rnd_datetime)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
