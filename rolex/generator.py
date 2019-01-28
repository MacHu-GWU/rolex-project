# -*- coding: utf-8 -*-

import random
from datetime import date, datetime, timedelta

try:  # pragma: no cover
    import numpy as np

    has_np = True
except:  # pragma: no cover
    has_np = False

from .pkg.sixmini import integer_types, string_types
from .parse import parser
from .util import (
    from_utctimestamp, to_utctimestamp,
    from_ordinal, to_ordinal,
)

_valid_freq = [
    "days", "day", "d",
    "hours", "hour", "h",
    "minutes", "minute", "min", "m",
    "seconds", "second", "sec", "s",
    "weeks", "week", "w",
]


def _freq_parser(freq):  # pragma: no cover
    """
    Parse frequency to timedelta.

    Valid keywords "days", "day", "d", "hours", "hour", "h",
    "minutes", "minute", "min", "m", "seconds", "second", "sec", "s",
    "weeks", "week", "w",
    """
    freq = freq.lower().strip()

    error_message = "'%s' is invalid, use one of %s" % (freq, _valid_freq)

    try:
        # day
        for surfix in ["days", "day", "d"]:
            if freq.endswith(surfix):
                freq = freq.replace(surfix, "")
                return timedelta(days=int(freq))

        # hour
        for surfix in ["hours", "hour", "h"]:
            if freq.endswith(surfix):
                freq = freq.replace(surfix, "")
                return timedelta(hours=int(freq))

        # minute
        for surfix in ["minutes", "minute", "min", "m"]:
            if freq.endswith(surfix):
                freq = freq.replace(surfix, "")
                return timedelta(minutes=int(freq))

        # second
        for surfix in ["seconds", "second", "sec", "s"]:
            if freq.endswith(surfix):
                freq = freq.replace(surfix, "")
                return timedelta(seconds=int(freq))

        # week
        for surfix in ["weeks", "week", "w"]:
            if freq.endswith(surfix):
                freq = freq.replace(surfix, "")
                return timedelta(days=int(freq) * 7)
    except:
        pass

    raise ValueError(error_message)


def time_series(start=None, end=None,
                periods=None, freq="1day",
                normalize=False, return_date=False):
    """
    A pure Python implementation of pandas.date_range().

    Given 2 of start, end, periods and freq, generate a series of
    datetime object.

    :param start: Left bound for generating dates
    :type start: str or datetime.datetime (default None)

    :param end: Right bound for generating dates
    :type end: str or datetime.datetime (default None)

    :param periods: Number of date points. If None, must specify start
        and end
    :type periods: integer (default None)

    :param freq: string, default '1day' (calendar daily)
        Available mode are day, hour, min, sec
        Frequency strings can have multiples. e.g.
            '7day', '6hour', '5min', '4sec', '3week`
    :type freq: string (default '1day' calendar daily)

    :param normalize: Trigger that normalize start/end dates to midnight
    :type normalize: boolean (default False)

    :param return_date: Trigger that only return date object.
    :type return_date: boolean (default False)

    :return: A list of datetime.datetime object. An evenly sampled time
        series.

    Usage::

        >>> from __future__ import print_function
        >>> for dt in rolex.time_series("2014-1-1", "2014-1-7"):
        ...     print(dt)
        2014-01-01 00:00:00
        2014-01-02 00:00:00
        2014-01-03 00:00:00
        2014-01-04 00:00:00
        2014-01-05 00:00:00
        2014-01-06 00:00:00
        2014-01-07 00:00:00

    **中文文档**

    生成等间隔的时间序列。

    需要给出, "起始", "结束", "数量" 中的任意两个。以及指定"频率"。以此唯一
    确定一个等间隔时间序列。"频率"项所支持的命令字符有"7day", "6hour",
    "5min", "4sec", "3week" (可以改变数字).
    """

    def normalize_datetime_to_midnight(dt):
        """Normalize a datetime %Y-%m-%d %H:%M:%S to %Y-%m-%d 00:00:00.
        """
        return datetime(dt.year, dt.month, dt.day)

    def not_normalize(dt):
        """Do not normalize.
        """
        return dt

    series = list()

    # if two of start, end, or periods exist
    if (bool(start) + bool(end) + bool(periods)) != 2:
        raise ValueError(
            "Must specify two of 'start', 'end', or 'periods'.")

    if normalize:
        converter = normalize_datetime_to_midnight
    else:
        converter = not_normalize

    interval = _freq_parser(freq)

    if (bool(start) & bool(end)):  # start and end
        start = parser.parse_datetime(start)
        end = parser.parse_datetime(end)
        _assert_correct_start_end(start, end)

        start = start - interval

        while 1:
            start += interval
            if start <= end:
                series.append(converter(start))
            else:
                break

    elif (bool(start) & bool(periods)):  # start and periods
        start = parser.parse_datetime(start)

        start = start - interval
        for _ in range(periods):
            start += interval
            series.append(converter(start))

    elif (bool(end) & bool(periods)):  # end and periods
        end = parser.parse_datetime(end)

        start = end - interval * periods
        for _ in range(periods):
            start += interval
            series.append(converter(start))

    if return_date:  # pragma: no cover
        series = [i.date() for i in series]

    return series


def weekday_series(start, end, weekday, return_date=False):
    """Generate a datetime series with same weekday number.

    ISO weekday number: Mon to Sun = 1 to 7

    Usage::

        >>> start, end = "2014-01-01 06:30:25", "2014-02-01 06:30:25"
        >>> rolex.weekday_series(start, end, weekday=2) # All Tuesday
        [
            datetime(2014, 1, 7, 6, 30, 25),
            datetime(2014, 1, 14, 6, 30, 25),
            datetime(2014, 1, 21, 6, 30, 25),
            datetime(2014, 1, 28, 6, 30, 25),
        ]

    :param weekday: int or list of int
    :returns: list of datetime

    **中文文档**

    生成星期数一致的时间序列。
    """
    start = parser.parse_datetime(start)
    end = parser.parse_datetime(end)
    _assert_correct_start_end(start, end)

    if isinstance(weekday, integer_types):
        weekday = [weekday, ]

    series = list()
    for i in time_series(start, end, freq="1day", return_date=return_date):
        if i.isoweekday() in weekday:
            series.append(i)

    return series


# --- Random Generator ---
def _randn(size, rnd_generator, *args, **kwargs):
    if isinstance(size, integer_types):
        if size < 0:
            raise ValueError("'size' can't smaller than zero")
        return [rnd_generator(*args, **kwargs) for _ in range(size)]
    else:
        try:
            m, n = size[0], size[1]
            if ((m < 0) or (n < 0)):
                raise ValueError("'size' can't smaller than zero")
            return [[rnd_generator(*args, **kwargs) for _ in range(n)] for _ in range(m)]
        except:
            raise ValueError("'size' has to be int or tuple. "
                             "e.g. 6 or (2, 3)")


def _assert_correct_start_end(start, end):
    if start > end:  # pragma: no cover
        raise ValueError("start time has to be earlier than end time!")


def _rnd_date(start, end):
    """Internal random date generator.
    """
    return date.fromordinal(random.randint(start.toordinal(), end.toordinal()))


def rnd_date(start=date(1970, 1, 1), end=None, **kwargs):
    """
    Generate a random date between ``start`` to ``end``.

    :param start: Left bound
    :type start: string or datetime.date, (default date(1970, 1, 1))
    :param end: Right bound
    :type end: string or datetime.date, (default date.today())
    :return: a datetime.date object

    **中文文档**

    随机生成一个位于 ``start`` 和 ``end`` 之间的日期。
    """
    if end is None:
        end = date.today()
    start = parser.parse_date(start)
    end = parser.parse_date(end)
    _assert_correct_start_end(start, end)
    return _rnd_date(start, end)


def rnd_date_array(size, start=date(1970, 1, 1), end=None, **kwargs):
    """
    Array or Matrix of random date generator.

    :returns: 1d or 2d array of datetime.date
    """
    if end is None:
        end = date.today()
    start = parser.parse_date(start)
    end = parser.parse_date(end)
    _assert_correct_start_end(start, end)
    return _randn(size, _rnd_date, start, end)


def rnd_date_list_high_performance(size, start=date(1970, 1, 1), end=None, **kwargs):
    """
    Generate mass random date.

    :param size: int, number of
    :param start: date similar object, int / str / date / datetime
    :param end: date similar object, int / str / date / datetime, default today's date
    :param kwargs: args placeholder
    :return: list of datetime.date
    """
    if end is None:
        end = date.today()
    start_days = to_ordinal(parser.parse_datetime(start))
    end_days = to_ordinal(parser.parse_datetime(end))
    _assert_correct_start_end(start_days, end_days)
    if has_np:  # pragma: no cover
        return [
            from_ordinal(days)
            for days in np.random.randint(start_days, end_days, size)
        ]
    else:
        return [
            from_ordinal(random.randint(start_days, end_days))
            for _ in range(size)
        ]


def _rnd_datetime(start, end):
    """
    Internal random datetime generator.
    """
    return from_utctimestamp(
        random.randint(
            int(to_utctimestamp(start)),
            int(to_utctimestamp(end)),
        )
    )


def rnd_datetime(start=datetime(1970, 1, 1), end=datetime.now()):
    """
    Generate a random datetime between ``start`` to ``end``.

    :param start: Left bound
    :type start: string or datetime.datetime, (default datetime(1970, 1, 1))
    :param end: Right bound
    :type end: string or datetime.datetime, (default datetime.now())
    :return: a datetime.datetime object

    **中文文档**

    随机生成一个位于 ``start`` 和 ``end`` 之间的时间。
    """
    start = parser.parse_datetime(start)
    end = parser.parse_datetime(end)
    _assert_correct_start_end(start, end)
    return _rnd_datetime(start, end)


def rnd_datetime_array(size, start=datetime(1970, 1, 1), end=None):
    """
    Array or Matrix of random datetime generator.

    :returns: 1d or 2d array of datetime.date
    """
    if end is None:
        end = datetime.now()
    start = parser.parse_datetime(start)
    end = parser.parse_datetime(end)
    _assert_correct_start_end(start, end)
    return _randn(size, _rnd_datetime, start, end)


def rnd_datetime_list_high_performance(size, start=datetime(1970, 1, 1), end=None):
    if end is None:
        end = datetime.now()
    start_ts = to_utctimestamp(parser.parse_datetime(start))
    end_ts = to_utctimestamp(parser.parse_datetime(end))
    _assert_correct_start_end(start, end)
    interval_range = end_ts - start_ts
    if has_np:  # pragma: no cover
        return [
            from_utctimestamp(v * interval_range + start_ts)
            for v in np.random.random(size)
        ]
    else:
        return [
            from_utctimestamp(random.random() * interval_range + start_ts)
            for _ in range(size)
        ]


def day_interval(year, month, day, milliseconds=False, return_string=False):
    """
    Return a start datetime and end datetime of a day.

    :param milliseconds: Minimum time resolution.
    :param return_string: If you want string instead of datetime, set True

    Usage Example::

        >>> start, end = rolex.day_interval(2014, 6, 17)
        >>> start
        datetime(2014, 6, 17, 0, 0, 0)

        >>> end
        datetime(2014, 6, 17, 23, 59, 59)
    """
    if milliseconds:  # pragma: no cover
        delta = timedelta(milliseconds=1)
    else:
        delta = timedelta(seconds=1)

    start = datetime(year, month, day)
    end = datetime(year, month, day) + timedelta(days=1) - delta

    if not return_string:
        return start, end
    else:
        return str(start), str(end)


def month_interval(year, month, milliseconds=False, return_string=False):
    """
    Return a start datetime and end datetime of a month.

    :param milliseconds: Minimum time resolution.
    :param return_string: If you want string instead of datetime, set True

    Usage Example::

        >>> start, end = rolex.month_interval(2000, 2)
        >>> start
        datetime(2000, 2, 1, 0, 0, 0)

        >>> end
        datetime(2000, 2, 29, 23, 59, 59)
    """
    if milliseconds:  # pragma: no cover
        delta = timedelta(milliseconds=1)
    else:
        delta = timedelta(seconds=1)

    if month == 12:
        start = datetime(year, month, 1)
        end = datetime(year + 1, 1, 1) - delta
    else:
        start = datetime(year, month, 1)
        end = datetime(year, month + 1, 1) - delta

    if not return_string:
        return start, end
    else:
        return str(start), str(end)


def year_interval(year, milliseconds=False, return_string=False):
    """
    Return a start datetime and end datetime of a year.

    :param milliseconds: Minimum time resolution.
    :param return_string: If you want string instead of datetime, set True

    Usage Example::

        >>> start, end = rolex.year_interval(2007)
        >>> start
        datetime(2007, 1, 1, 0, 0, 0)

        >>> end
        datetime(2007, 12, 31, 23, 59, 59)
    """
    if milliseconds:  # pragma: no cover
        delta = timedelta(milliseconds=1)
    else:
        delta = timedelta(seconds=1)

    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1) - delta

    if not return_string:
        return start, end
    else:
        return str(start), str(end)
