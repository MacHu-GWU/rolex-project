#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
try:
    from .parse import parser
except:  # pragma: no cover
    from rolex.parse import parser


#--- Calculator ---
def add_seconds(datetime_like_object, n, return_date=False):
    """
    Returns a time that n seconds after a time.

    :param datetimestr: a datetime object or a datetime str
    :param n: number of seconds, value can be negative

    **中文文档**

    返回给定日期N秒之后的时间。
    """
    a_datetime = parser.parse_datetime(datetime_like_object)
    a_datetime = a_datetime + timedelta(seconds=n)
    if return_date:  # pragma: no cover
        return a_datetime.date()
    else:
        return a_datetime


def add_minutes(datetime_like_object, n, return_date=False):
    """
    Returns a time that n minutes after a time.

    :param datetimestr: a datetime object or a datetime str
    :param n: number of minutes, value can be negative

    **中文文档**

    返回给定日期N分钟之后的时间。
    """
    return add_seconds(datetime_like_object, n * 60, return_date)


def add_hours(datetime_like_object, n, return_date=False):
    """
    Returns a time that n hours after a time.

    :param datetimestr: a datetime object or a datetime str
    :param n: number of hours, value can be negative

    **中文文档**

    返回给定日期N小时之后的时间。
    """
    return add_seconds(datetime_like_object, n * 60 * 60, return_date)


def add_days(datetime_like_object, n, return_date=False):
    """
    Returns a time that n days after a time.

    :param datetimestr: a datetime object or a datetime str
    :param n: number of days, value can be negative
    :param return_date: returns a date object instead of datetime

    **中文文档**

    返回给定日期N天之后的时间。
    """
    return add_seconds(datetime_like_object, n * 60 * 60 * 24, return_date)


def add_weeks(datetime_like_object, n, return_date=False):
    """
    Returns a time that n weeks after a time.

    :param datetimestr: a datetime object or a datetime str
    :param n: number of weeks, value can be negative
    :param return_date: returns a date object instead of datetime

    **中文文档**

    返回给定日期N周之后的时间。
    """
    return add_seconds(datetime_like_object, n * 60 * 60 * 24 * 7, return_date)


def add_months(datetime_like_object, n, return_date=False):
    """
    Returns a time that n months after a time.

    Notice: for example, the date that one month after 2015-01-31 supposed
    to be 2015-02-31. But there's no 31th in Feb, so we fix that value to
    2015-02-28.

    :param datetimestr: a datetime object or a datetime str
    :param n: number of months, value can be negative
    :param return_date: returns a date object instead of datetime

    **中文文档**

    返回给定日期N月之后的时间。
    """
    a_datetime = parser.parse_datetime(datetime_like_object)
    month_from_ordinary = a_datetime.year * 12 + a_datetime.month
    month_from_ordinary += n
    year, month = divmod(month_from_ordinary, 12)

    # try assign year, month, day
    try:
        a_datetime = datetime(
            year, month, a_datetime.day,
            a_datetime.hour, a_datetime.minute, a_datetime.second,
            a_datetime.microsecond, tzinfo=a_datetime.tzinfo,
        )
    # 肯定是由于新的月份的日子不够, 所以肯定是月底,
    # 那么直接跳到下一个月的第一天, 再回退一天
    except ValueError:
        month_from_ordinary += 1
        year, month = divmod(month_from_ordinary, 12)
        a_datetime = datetime(
            year, month, 1,
            a_datetime.hour, a_datetime.minute, a_datetime.second,
            a_datetime.microsecond, tzinfo=a_datetime.tzinfo,
        )
        a_datetime = add_days(a_datetime, -1)

    if return_date:  # pragma: no cover
        return a_datetime.date()
    else:
        return a_datetime


def add_years(datetime_like_object, n, return_date=False):
    """
    Returns a time that n years after a time.

    :param datetimestr: a datetime object or a datetime str
    :param n: number of years, value can be negative
    :param return_date: returns a date object instead of datetime

    **中文文档**

    返回给定日期N年之后的时间。
    """
    a_datetime = parser.parse_datetime(datetime_like_object)

    # try assign year, month, day
    try:
        a_datetime = datetime(
            a_datetime.year + n, a_datetime.month, a_datetime.day,
            a_datetime.hour, a_datetime.minute, a_datetime.second,
            a_datetime.microsecond, tzinfo=a_datetime.tzinfo,
        )
    except ValueError:  # Must be xxxx-02-29
        a_datetime = datetime(
            a_datetime.year + n, 2, 28,
            a_datetime.hour, a_datetime.minute,
            a_datetime.second, a_datetime.microsecond)

    if return_date:  # pragma: no cover
        return a_datetime.date()
    else:
        return a_datetime


def _floor_to(dt, hour, minute, second):
    """
    Route the given datetime to the latest time with the hour, minute, second
    before it.
    """
    new_dt = dt.replace(hour=hour, minute=minute, second=second)
    if new_dt <= dt:
        return new_dt
    else:
        return new_dt - timedelta(days=1)


def _ceiling_to(dt, hour, minute, second):
    """
    Route the given datetime to the earliest time with the hour, minute, second
    after it.
    """
    new_dt = dt.replace(hour=hour, minute=minute, second=second)
    if new_dt >= dt:
        return new_dt
    else:
        return new_dt + timedelta(days=1)


def _round_to(dt, hour, minute, second):
    """
    Route the given datetime to the latest time with the hour, minute, second
    before it.
    """
    new_dt = dt.replace(hour=hour, minute=minute, second=second)
    if new_dt == dt:
        return new_dt
    elif new_dt < dt:
        before = new_dt
        after = new_dt + timedelta(days=1)
    elif new_dt > dt:
        before = new_dt - timedelta(days=1)
        after = new_dt

    d1 = dt - before
    d2 = after - dt

    if d1 < d2:
        return before
    elif d1 > d2:
        return after
    else:
        return before


from collections import OrderedDict

_round_to_options = OrderedDict([
    ("floor", _floor_to),
    ("ceiling", _ceiling_to),
    ("round", _round_to),
])


def round_to(dt, hour, minute, second, mode="round"):
    """
    Round the given datetime to specified hour, minute and second.

    :param mode: 'floor' or 'ceiling'

    .. versionadded:: 0.0.5

        message


    **中文文档**

    将给定时间对齐到最近的一个指定了小时, 分钟, 秒的时间上。
    """
    mode = mode.lower()
    if mode not in _round_to_options:
        raise ValueError(
            "'mode' has to be one of %r!" % list(_round_to_options.keys()))
    return _round_to_options[mode](dt, hour, minute, second)
