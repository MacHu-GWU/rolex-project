#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.3"
__short_description__ = "An elegant datetime library."
__license__ = "MIT"
__author__ = "Sanhe Hu"

import random
from datetime import datetime, date, timedelta, tzinfo

try:
    from dateutil import parser
except ImportError as e:
    print("Please install python_dateutil!")

try:
    from .six import PY3, string_types, integer_types
    from .template import DateTemplates, DatetimeTemplates
except:
    from rolex.six import PY3, string_types, integer_types
    from rolex.template import DateTemplates, DatetimeTemplates

ZERO = timedelta(0)


class UTC(tzinfo):
    """UTC
    """

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()


class Rolex(object):
    """Main class. A time related utility class.

    Abbreviations:

    - dt -> datetime object
    - d -> date object
    - ts -> timestamp
    - s -> string
    - i -> int/item

    **中文文档**

    本类提供了非常多与时间, 日期相关的函数。其中

    "时间包装器"提供了对时间, 日期相关的许多计算操作的函数。能智能的从各种其他
    格式的时间中解析出Python datetime.datetime/datetime.date 对象。更多功能请
    参考API文档。
    """
    DateTemplates = DateTemplates
    DatetimeTemplates = DatetimeTemplates
    default_date_template = DatetimeTemplates[0]
    default_datetime_template = DatetimeTemplates[0]

    #--- Parse datetime ---
    def str2date(self, datestr):
        """Parse date from string. If no template matches this string,
        raise Error. Please go
        https://github.com/MacHu-GWU/rolex-project/issues
        submit your date string. I 'll update templates asap.

        This method is faster than :meth:`dateutil.parser.parse`.

        :param datestr: a string represent a date
        :type datestr: str
        :return: a date object

        **中文文档**

        从string解析date。首先尝试默认模板, 如果失败了, 则尝试所有的模板。
        一旦尝试成功, 就将当前成功的模板保存为默认模板。这样做在当你待解析的
        字符串非常多, 且模式单一时, 只有第一次尝试耗时较多, 之后就非常快了。
        该方法要快过 :meth:`dateutil.parser.parse` 方法。
        """
        # try default date template
        try:
            return datetime.strptime(
                datestr, self.default_date_template).date()
        except:
            pass

        # try every datetime templates
        for template in DateTemplates:
            try:
                dt = datetime.strptime(datestr, template)
                self.default_date_template = template
                return dt.date()
            except:
                pass

        # raise error
        raise Exception("Unable to parse date from: %r" % datestr)
            
    def _str2datetime(self, datetimestr):
        """Parse datetime from string. If no template matches this string,
        raise Error. Please go
        https://github.com/MacHu-GWU/rolex-project/issues
        submit your datetime string. I 'll update templates asap.

        This method is faster than :meth:`dateutil.parser.parse`.

        :param datetimestr: a string represent a datetime
        :type datetimestr: str
        :return: a datetime object

        **中文文档**

        从string解析datetime。首先尝试默认模板, 如果失败了, 则尝试所有的模板。
        一旦尝试成功, 就将当前成功的模板保存为默认模板。这样做在当你待解析的
        字符串非常多, 且模式单一时, 只有第一次尝试耗时较多, 之后就非常快了。
        该方法要快过 :meth:`dateutil.parser.parse` 方法。
        """
        # try default datetime template
        try:
            return datetime.strptime(
                datetimestr, self.default_datetime_template)
        except:
            pass

        # try every datetime templates
        for template in DatetimeTemplates:
            try:
                dt = datetime.strptime(datetimestr, template)
                self.default_datetime_template = template
                return dt
            except:
                pass

        # raise error
        dt = parser.parse(datetimestr)
        self.str2datetime = parser.parse
        
        return dt
        
    str2datetime = _str2datetime
    
    def parse_date(self, value):
        """A lazy method to parse anything to date.

        If input data type is:

        - string: parse date from it
        - integer: use from ordinal
        - datetime: use date part
        - date: just return it
        """
        if isinstance(value, str):
            return self.str2date(value)
        elif isinstance(value, int):
            return date.fromordinal(value)
        elif isinstance(value, datetime):
            return value.date()
        elif isinstance(value, date):
            return value
        else:
            raise Exception("Unable to parse date from %r" % value)

    def parse_datetime(self, value):
        """A lazy method to parse anything to datetime.

        If input data type is:

        - string: parse datetime from it
        - integer: use from ordinal
        - date: use date part and set hour, minute, second to zero
        - datetime: just return it
        """
        if isinstance(value, str):
            return self.str2datetime(value)
        elif isinstance(value, integer_types):
            return self.from_utctimestamp(value)
        elif isinstance(value, float):
            return self.from_utctimestamp(value)
        elif isinstance(value, datetime):
            return value
        elif isinstance(value, date):
            return datetime(value.year, value.month, value.day)
        else:
            raise Exception("Unable to parse datetime from %r" % value)

    #--- Method extension toordinary, timestamp ---
    def to_ordinal(self, date_object):
        """Calculate number of days from 0000-00-00.
        """
        return date_object.toordinal()

    def from_ordinal(self, days):
        """Create a date object that number ``days`` of days after 0000-00-00.
        """
        return date.fromordinal(days)

    def to_utctimestamp(self, dt):
        """Calculate number of seconds from UTC 1970-01-01 00:00:00.

        When:

        - dt doesn't have tzinfo: assume it's a utc time
        - dt has tzinfo: use tzinfo

        WARNING, if your datetime object doens't have ``tzinfo``, make sure
        it's a UTC time, but **NOT a LOCAL TIME**.

        **中文文档**

        计算时间戳

        若:

        - 不带tzinfo: 则默认为是UTC time
        - 带tzinfo: 使用tzinfo
        """
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=utc)
        delta = dt - datetime(1970, 1, 1, tzinfo=utc)
        return delta.total_seconds()

    def from_utctimestamp(self, timestamp):
        """Create a **UTC datetime** object that number of seconds after
        UTC 1970-01-01 00:00:00. If you want local time, use
        :meth:`Rolex.from_timestamp`

        Because python doesn't support negative timestamp to datetime
        so we have to implement my own method.

        **中文文档**

        返回一个在UTC 1970-01-01 00:00:00 之后 #timestamp 秒后的时间。默认为
        UTC时间。即返回的datetime不带tzinfo
        """
        if timestamp >= 0:
            return datetime.utcfromtimestamp(timestamp)
        else:
            return datetime(1970, 1, 1) + timedelta(seconds=timestamp)

    def to_timestamp(self, dt):
        """Calculate number of seconds from UTC 1970-01-01 00:00:00.

        When:

        - dt doesn't have tzinfo: assume it's a local time on your computer
        - dt has tzinfo: use tzinfo

        **中文文档**

        计算时间戳

        若:

        - 不带tzinfo: 则默认为是本机的local time
        - 带tzinfo: 使用tzinfo
        """
        if PY3:
            return dt.timestamp()
        else:
            raise SystemError("Python2 doesn't support this method!")

    def from_timestamp(self, timestamp):
        """Create a **local datetime** object that number of seconds after
        UTC 1970-01-01 00:00:00. If you want utc time, use
        :meth:`Rolex.from_utctimestamp`

        **中文文档**

        根据时间戳, 计算时间, 返回的是你的本机local time的时间。
        """
        if timestamp >= 0:
            return datetime.fromtimestamp(timestamp)
        else:
            return datetime.fromtimestamp(0) - timedelta(seconds=-timestamp)

    #--- Time series ---
    def _freq_parser(self, freq):
        """Parse timedelta.

        Valid keywords "days", "day", "d", "hours", "hour", "h",
        "minutes", "minute", "min", "m", "seconds", "second", "sec", "s",
        "weeks", "week", "w",
        """
        freq = freq.lower().strip()

        valid_keywords = [
            "days", "day", "d",
            "hours", "hour", "h",
            "minutes", "minute", "min", "m",
            "seconds", "second", "sec", "s",
            "weeks", "week", "w",
        ]
        error_message = "'%s' is invalid, use one of %s" % (
            freq, valid_keywords)

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

    def time_series(self, start=None, end=None, periods=None,
                    freq="1day", normalize=False, return_date=False):
        """A pure Python implementation of pandas.date_range().
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

        interval = self._freq_parser(freq)

        if (bool(start) & bool(end)):  # start and end
            start = self.parse_datetime(start)
            end = self.parse_datetime(end)

            if start > end:  # if start time later than end time, raise error
                raise ValueError("start time has to be earlier than end time")

            start = start - interval

            while 1:
                start += interval
                if start <= end:
                    series.append(converter(start))
                else:
                    break

        elif (bool(start) & bool(periods)):  # start and periods
            start = self.parse_datetime(start)

            start = start - interval
            for _ in range(periods):
                start += interval
                series.append(converter(start))

        elif (bool(end) & bool(periods)):  # end and periods
            end = self.parse_datetime(end)

            start = end - interval * periods
            for _ in range(periods):
                start += interval
                series.append(converter(start))

        if return_date:
            series = [i.date() for i in series]

        return series

    def weekday_series(self, start, end, weekday, return_date=False):
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

        **中文文档**

        生成星期数一致的时间序列。
        """
        start = self.parse_datetime(start)
        end = self.parse_datetime(end)

        if isinstance(weekday, integer_types):
            weekday = [weekday, ]

        series = list()
        for i in self.time_series(
                start, end, freq="1day", return_date=return_date):
            if i.isoweekday() in weekday:
                series.append(i)

        return series

    def isweekend(self, d_or_dt):
        """Check if a datetime is weekend.
        """
        return d_or_dt.isoweekday() in [6, 7]

    def isweekday(self, d_or_dt):
        """Check if a datetime is weekday.
        """
        return d_or_dt.isoweekday() not in [6, 7]

    #--- Random Generator ---
    def randn(self, size, rnd_generator, *args):
        if isinstance(size, integer_types):
            if size < 0:
                raise ValueError("'size' can't smaller than zero")
            return [rnd_generator(*args) for _ in range(size)]
        else:
            try:
                m, n = size[0], size[1]
                if ((m < 0) or (n < 0)):
                    raise ValueError("'size' can't smaller than zero")
                return [[rnd_generator(*args) for _ in range(n)] for _ in range(m)]
            except:
                raise ValueError("'size' has to be int or tuple. "
                                 "e.g. 6 or (2, 3)")

    def _rnd_date(self, start, end):
        """Internal random date generator.
        """
        return date.fromordinal(
            random.randint(start.toordinal(), end.toordinal()))

    def rnd_date(self, start=date(1970, 1, 1), end=date.today()):
        """Generate a random date between ``start`` to ``end``.

        :param start: Left bound
        :type start: string or datetime.date, (default date(1970, 1, 1))
        :param end: Right bound
        :type end: string or datetime.date, (default date.today())
        :return: a datetime.date object

        **中文文档**

        随机生成一个位于 ``start`` 和 ``end`` 之间的日期。
        """
        if isinstance(start, str):
            start = self.str2date(start)
        if isinstance(end, str):
            end = self.str2date(end)
        if start > end:
            raise ValueError("start time has to be earlier than end time")
        return date.fromordinal(
            random.randint(start.toordinal(), end.toordinal()))

    def rnd_date_array(self, size, start=date(1970, 1, 1), end=date.today()):
        """Array or Matrix of random date generator.
        """
        if isinstance(start, str):
            start = self.str2date(start)
        if isinstance(end, str):
            end = self.str2date(end)
        if start > end:
            raise ValueError("start time has to be earlier than end time")

        return self.randn(size, self._rnd_date, start, end)

    def _rnd_datetime(self, start, end):
        """Internal random datetime generator.
        """
        return self.from_utctimestamp(
            random.randint(
                int(self.to_utctimestamp(start)),
                int(self.to_utctimestamp(end)),
            )
        )

    def rnd_datetime(self, start=datetime(1970, 1, 1), end=datetime.now()):
        """Generate a random datetime between ``start`` to ``end``.

        :param start: Left bound
        :type start: string or datetime.datetime, (default datetime(1970, 1, 1))
        :param end: Right bound
        :type end: string or datetime.datetime, (default datetime.now())
        :return: a datetime.datetime object

        **中文文档**

        随机生成一个位于 ``start`` 和 ``end`` 之间的时间。
        """
        if isinstance(start, str):
            start = self.str2datetime(start)
        if isinstance(end, str):
            end = self.str2datetime(end)
        if start > end:
            raise ValueError("start time has to be earlier than end time")
        return self.from_utctimestamp(
            random.randint(
                int(self.to_utctimestamp(start)),
                int(self.to_utctimestamp(end)),
            )
        )

    def rnd_datetime_array(self,
                           size, start=datetime(1970, 1, 1), end=datetime.now()):
        """Array or Matrix of random datetime generator.
        """
        if isinstance(start, str):
            start = self.str2datetime(start)
        if isinstance(end, str):
            end = self.str2datetime(end)
        if start > end:
            raise ValueError("start time has to be earlier than end time")

        return self.randn(size, self._rnd_datetime, start, end)

    #--- Calculator ---
    def add_seconds(self, datetimestr, n):
        """Returns a time that n seconds after a time.

        :param datetimestr: a datetime object or a datetime str
        :param n: number of seconds, value can be negative

        **中文文档**

        返回给定日期N秒之后的时间。
        """
        a_datetime = self.parse_datetime(datetimestr)
        return a_datetime + timedelta(seconds=n)

    def add_minutes(self, datetimestr, n):
        """Returns a time that n minutes after a time.

        :param datetimestr: a datetime object or a datetime str
        :param n: number of minutes, value can be negative

        **中文文档**

        返回给定日期N分钟之后的时间。
        """
        a_datetime = self.parse_datetime(datetimestr)
        return a_datetime + timedelta(seconds=60 * n)

    def add_hours(self, datetimestr, n):
        """Returns a time that n hours after a time.

        :param datetimestr: a datetime object or a datetime str
        :param n: number of hours, value can be negative

        **中文文档**

        返回给定日期N小时之后的时间。
        """
        a_datetime = self.parse_datetime(datetimestr)
        return a_datetime + timedelta(seconds=3600 * n)

    def add_days(self, datetimestr, n, return_date=False):
        """Returns a time that n days after a time.

        :param datetimestr: a datetime object or a datetime str
        :param n: number of days, value can be negative
        :param return_date: returns a date object instead of datetime

        **中文文档**

        返回给定日期N天之后的时间。
        """
        a_datetime = self.parse_datetime(datetimestr)
        a_datetime += timedelta(days=n)
        if return_date:
            return a_datetime.date()
        else:
            return a_datetime

    def add_weeks(self, datetimestr, n, return_date=False):
        """Returns a time that n weeks after a time.

        :param datetimestr: a datetime object or a datetime str
        :param n: number of weeks, value can be negative
        :param return_date: returns a date object instead of datetime

        **中文文档**

        返回给定日期N周之后的时间。
        """
        a_datetime = self.parse_datetime(datetimestr)
        a_datetime += timedelta(days=7 * n)
        if return_date:
            return a_datetime.date()
        else:
            return a_datetime

    def add_months(self, datetimestr, n, return_date=False):
        """Returns a time that n months after a time.

        Notice: for example, the date that one month after 2015-01-31 supposed
        to be 2015-02-31. But there's no 31th in Feb, so we fix that value to
        2015-02-28.

        :param datetimestr: a datetime object or a datetime str
        :param n: number of months, value can be negative
        :param return_date: returns a date object instead of datetime

        **中文文档**

        返回给定日期N月之后的时间。
        """
        a_datetime = self.parse_datetime(datetimestr)
        month_from_ordinary = a_datetime.year * 12 + a_datetime.month
        month_from_ordinary += n
        year, month = divmod(month_from_ordinary, 12)

        # 尝试直接assign year, month, day
        try:
            a_datetime = datetime(year, month, a_datetime.day,
                                  a_datetime.hour, a_datetime.minute,
                                  a_datetime.second, a_datetime.microsecond)
        # 肯定是由于新的月份的日子不够, 那么直接跳到下一个月的第一天, 再回退一天
        except ValueError:
            a_datetime = datetime(year, month + 1, 1,
                                  a_datetime.hour, a_datetime.minute,
                                  a_datetime.second, a_datetime.microsecond)
            a_datetime = self.add_days(a_datetime, -1)

        if return_date:
            return a_datetime.date()
        else:
            return a_datetime

    def add_years(self, datetimestr, n, return_date=False):
        """Returns a time that n years after a time.

        :param datetimestr: a datetime object or a datetime str
        :param n: number of years, value can be negative
        :param return_date: returns a date object instead of datetime

        **中文文档**

        返回给定日期N年之后的时间。
        """
        a_datetime = self.parse_datetime(datetimestr)

        try:
            a_datetime = datetime(
                a_datetime.year + n, a_datetime.month, a_datetime.day,
                a_datetime.hour, a_datetime.minute,
                a_datetime.second, a_datetime.microsecond)
        except:
            a_datetime = datetime(
                a_datetime.year + n, 2, 28,
                a_datetime.hour, a_datetime.minute,
                a_datetime.second, a_datetime.microsecond)

        if return_date:
            return a_datetime.date()
        else:
            return a_datetime

    def round_to(self, dt, hour, minute, second, mode="floor"):
        """Round the given datetime to specified hour, minute and second.

        :param mode: 'floor' or 'ceiling'

        **中文文档**

        将给定时间对齐到最近的一个指定了小时, 分钟, 秒的时间上。
        """
        mode = mode.lower()

        new_dt = datetime(dt.year, dt.month, dt.day, hour, minute, second)
        if mode == "floor":
            if new_dt <= dt:
                return new_dt
            else:
                return rolex.add_days(new_dt, -1)
        elif mode == "ceiling":
            if new_dt >= dt:
                return new_dt
            else:
                return rolex.add_days(new_dt, 1)
        else:
            raise ValueError("'mode' has to be 'floor' or 'ceiling'!")

    @staticmethod
    def day_interval(year, month, day, milliseconds=False, return_string=False):
        """Return a start datetime and end datetime of a day.

        :param milliseconds: Minimum time resolution.
        :param return_string: If you want string instead of datetime, set True

        Usage Example::

            >>> start, end = rolex.day_interval(2014, 6, 17)
            >>> start
            datetime(2014, 6, 17, 0, 0, 0)

            >>> end
            datetime(2014, 6, 17, 23, 59, 59)
        """
        if milliseconds:
            delta = timedelta(milliseconds=1)
        else:
            delta = timedelta(seconds=1)

        start = datetime(year, month, day)
        end = datetime(year, month, day) + timedelta(days=1) - delta

        if not return_string:
            return start, end
        else:
            return str(start), str(end)

    @staticmethod
    def month_interval(year, month, milliseconds=False, return_string=False):
        """Return a start datetime and end datetime of a month.

        :param milliseconds: Minimum time resolution.
        :param return_string: If you want string instead of datetime, set True

        Usage Example::

            >>> start, end = rolex.month_interval(2000, 2)
            >>> start
            datetime(2000, 2, 1, 0, 0, 0)

            >>> end
            datetime(2000, 2, 29, 23, 59, 59)
        """
        if milliseconds:
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

    @staticmethod
    def year_interval(year, milliseconds=False, return_string=False):
        """Return a start datetime and end datetime of a year.

        :param milliseconds: Minimum time resolution.
        :param return_string: If you want string instead of datetime, set True

        Usage Example::

            >>> start, end = rolex.year_interval(2007)
            >>> start
            datetime(2007, 1, 1, 0, 0, 0)

            >>> end
            datetime(2007, 12, 31, 23, 59, 59)
        """
        if milliseconds:
            delta = timedelta(milliseconds=1)
        else:
            delta = timedelta(seconds=1)

        start = datetime(year, 1, 1)
        end = datetime(year + 1, 1, 1) - delta

        if not return_string:
            return start, end
        else:
            return str(start), str(end)

rolex = Rolex()
