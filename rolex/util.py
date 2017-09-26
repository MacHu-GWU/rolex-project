#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
time math calculation.
"""

from datetime import date, datetime, timedelta

try:
    from .tz import utc, local
except:  # pragma: no cover
    from rolex.tz import utc, local


def to_ordinal(a_date):
    """
    Calculate number of days from 0000-00-00.
    """
    return a_date.toordinal()


def from_ordinal(days):
    """
    Create a date object that number ``days`` of days after 0000-00-00.
    """
    return date.fromordinal(days)


def to_utctimestamp(a_datetime):
    """
    Calculate number of seconds from UTC 1970-01-01 00:00:00.

    When:

    - dt doesn't have tzinfo: assume it's a utc time.
    - dt has tzinfo: use tzinfo.

    WARNING, if your datetime object doens't have ``tzinfo``, make sure
    it's a UTC time, but **NOT a LOCAL TIME**.

    **中文文档**

    计算时间戳, 若:

    - 不带tzinfo: 则默认为是UTC time。
    - 带tzinfo: 则使用tzinfo。
    """
    if a_datetime.tzinfo is None:
        delta = a_datetime - datetime(1970, 1, 1)
    else:
        delta = a_datetime - datetime(1970, 1, 1, tzinfo=utc)
    return delta.total_seconds()


def from_utctimestamp(timestamp):
    """
    Create a **datetime** object that number of seconds after
    UTC 1970-01-01 00:00:00. If you want local time, use
    :meth:`from_timestamp`

    This method support negative timestamp.

    :returns: non-timezone awared UTC datetime.

    **中文文档**

    返回一个在UTC 1970-01-01 00:00:00 之后 #timestamp 秒后的时间。默认为
    UTC时间。即返回的datetime不带tzinfo
    """
    return datetime(1970, 1, 1) + timedelta(seconds=timestamp)


def to_utc(a_datetime, keep_utc_tzinfo=False):
    """
    Convert a time awared datetime to utc datetime.

    :param a_datetime: a timezone awared datetime. (If not, then just returns)
    :param keep_utc_tzinfo: whether to retain the utc time zone information.

    **中文文档**

    将一个带时区的时间转化成UTC时间。而对于UTC时间而言, 有没有时区信息都无所谓了。
    """
    if a_datetime.tzinfo:
        utc_datetime = a_datetime.astimezone(utc)  # convert to utc time
        if keep_utc_tzinfo is False:
            utc_datetime = utc_datetime.replace(tzinfo=None)
        return utc_datetime
    else:
        return a_datetime


def utc_to_tz(utc_datetime, tzinfo, keep_tzinfo=False):
    """
    Convert a UTC datetime to a time awared local time

    :param utc_datetime:
    :param tzinfo:
    :param keep_tzinfo:
    """
    tz_awared_datetime = utc_datetime.replace(tzinfo=utc).astimezone(tzinfo)
    if keep_tzinfo is False:
        tz_awared_datetime = tz_awared_datetime.replace(tzinfo=None)
    return tz_awared_datetime


def utc_to_local(utc_datetime, keep_tzinfo=False):
    """
    Convert a UTC datetime to current machine local timezone datetime.

    :param utc_datetime:
    :param keep_tzinfo:
    """
    return utc_to_tz(utc_datetime, local, keep_tzinfo)


def is_weekend(d_or_dt):
    """Check if a datetime is weekend.
    """
    return d_or_dt.isoweekday() in [6, 7]


def is_weekday(d_or_dt):
    """Check if a datetime is weekday.
    """
    return d_or_dt.isoweekday() not in [6, 7]
