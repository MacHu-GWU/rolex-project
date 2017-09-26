#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import pytest
from pytest import raises, approx

from datetime import date, datetime
from dateutil.parser import parse
from rolex.parse import (
    date_template_and_example,
    datetime_template_and_example,
    parser,
)


def test_template():
    for tpl, example in date_template_and_example:
        datetime.strptime(example, tpl).date()

    for tpl, example in datetime_template_and_example:
        datetime.strptime(example, tpl)


class TestParser(object):
    def test_str2date(self):
        assert parser.str2date("9/21/2014") == date(2014, 9, 21)
        assert parser._default_date_template == "%m/%d/%Y"

    def test_str2date_error(self):
        with raises(ValueError):
            parser.str2date("1234567890")

    def test_str2datetime(self):
        assert parser.str2datetime(
            "2014-07-13 8:12:34 PM") == datetime(2014, 7, 13, 20, 12, 34)
        assert parser._default_datetime_template == "%Y-%m-%d %I:%M:%S %p"
        assert parser.str2datetime.__name__ == "_str2datetime"

        # When rolex failed to parse date time string,
        # then start using dateutil.parser.parse
        assert isinstance(parser.str2datetime("2000-01-01T00:00:00-5"),
                          datetime)
        assert parser.str2datetime.__name__ == "parse"

        # You can use .reset() method to restore default behavior
        parser.reset()
        assert parser.str2datetime.__name__ == "_str2datetime"

    def test_performance(self):
        """Test Result:

        - rolex is 4 ~ 5 times faster than dateutil.
        - rolex support more data type, can take string, timestamp, date or datetime

        Result::

            10 item, rolex takes 0.000239 sec, dateutil takes 0.001051 sec.
            100 item, rolex takes 0.002138 sec, dateutil takes 0.009662 sec.
            1000 item, rolex takes 0.021126 sec, dateutil takes 0.097736 sec.
            10000 item, rolex takes 0.214618 sec, dateutil takes 0.977337 sec.
        """
        import time
        import random

        parser.reset()

        tested_datetime_template_list = [
            "%Y-%m-%d %I:%M:%S %p",
            "%Y-%m-%dT%H:%M:%S.%fZ%Z",
            "%a, %d %b %Y %H:%M:%S GMT",
        ]
        tpl = random.choice(tested_datetime_template_list)
        print("datetime format is: %r" % tpl)
        for n in [10 ** n for n in range(2, 3 + 1)]:
            data = [datetime.strftime(datetime.now(), tpl) \
                    for _ in range(n)]

            st = time.clock()
            for datetime_str in data:
                parser.str2datetime(datetime_str)
            elapse1 = time.clock() - st

            st = time.clock()
            for datetime_str in data:
                parse(datetime_str)
            elapse2 = time.clock() - st

            print("%s item, rolex takes %.6f sec, "
                  "dateutil takes %.6f sec, "
                  "rolex is %.2f times faster than dateutil." % (
                      n, elapse1, elapse2, elapse2 / elapse1))

    def test_parse_date(self):
        """parse anything to date.
        """
        assert parser.parse_date("12-1-2000") == date(2000, 12, 1)
        with raises(TypeError):
            parser.parse_date(None)
        assert parser.parse_date(730120) == date(2000, 1, 1)
        assert parser.parse_date(datetime(2000, 1, 1)) == date(2000, 1, 1)
        assert parser.parse_date(date(2000, 1, 1)) == date(2000, 1, 1)
        with raises(ValueError):
            parser.parse_date([1, 2, 3])

    def test_parse_datetime(self):
        """parse anything to datetime.
        """
        assert parser.parse_datetime(
            "2000-1-1 8:15:00") == datetime(2000, 1, 1, 8, 15)
        with raises(TypeError):
            parser.parse_datetime(None)
        assert parser.parse_datetime(1) == datetime(1970, 1, 1, 0, 0, 1)
        assert parser.parse_datetime(-1.0) == datetime(1969, 12, 31, 23, 59, 59)
        assert parser.parse_datetime(
            datetime(2000, 1, 1, 8, 30, 0)) == datetime(2000, 1, 1, 8, 30, 0)
        assert parser.parse_datetime(date(2000, 1, 1)) == datetime(2000, 1, 1)
        with raises(ValueError):
            parser.parse_datetime([1, 2, 3])


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
