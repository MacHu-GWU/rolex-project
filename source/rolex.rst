The Convenience of Using rolex
==============================
First, let's import::

	from rolex import rolex
	from datetime import datetime, date


Parser
------

Parse anything to ``datetime``::

	>>> rolex.parse_datetime("2014-01-15T17:58:31Z-0400")
	datetime.datetime(2014, 1, 15, 17, 58, 31, tzinfo=datetime.timezone(datetime.timedelta(-1, 72000)))

	>>> rolex.parse_datetime(1234567890)
	datetime.datetime(2009, 2, 13, 23, 31, 30)

	>>> rolex.parse_datetime(date(2015, 12, 24))
	datetime.datetime(2015, 12, 24, 0, 0)

	>>> rolex.parse_datetime(datetime(2015, 11, 24, 20, 30))
	datetime.datetime(2015, 11, 24, 20, 30)

Also works fine with ``date``::

	>>> rolex.parse_date("Saturday, September 20, 2014")
	datetime.date(2014, 9, 20)

	>>> rolex.parse_date(720000)
	datetime.date(1972, 4, 17)

	...

If rolex failed to parse it from string, automatically, it will start using `dateutil <https://dateutil.readthedocs.io/en/stable/>`_, so if rolex can't parse the string, then dateutil also can't. **But rolex's built in method is 4x times faster** than ``dateutil`` for recognized pattern. If ``rolex`` failed to parse your string, **please submit it to** https://github.com/MacHu-GWU/rolex-project/issues.


Timestamp
---------
Python2 doens't implement ``datetime.timestamp()``, and also it assume that it's a local time by default. **That's not good**!

``rolex`` provide more flexibility:

- :meth:`~rolex.Rolex.to_timestamp()`: assume it's local time if it is a naive datetime
- :meth:`~rolex.Rolex.to_utctimestamp()`: assume it's utc time if it is a naive datetime
- :meth:`~rolex.Rolex.from_timestamp()`: return a utc time represent of a utc timestamp
- :meth:`~rolex.Rolex.from_utctimestamp()`: return a local time represent of a utc timestamp

Plus, :meth:`~rolex.Rolex.to_ordinal()`, :meth:`~rolex.Rolex.from_ordinal()` are very useful.


Random Generator
----------------
As simple as this::

	>>> rolex.rnd_date("2015-01-01", "2015-12-31")
	datetime.date(2015, 5, 14)

	>>> rolex.rnd_date_array(10, "2015-01-01", "2015-12-31") # gives you length-6 date list

	>>> rolex.rnd_date_array((2, 3), "2015-01-01", "2015-12-31") # gives you 2 x 3 date matrix

:meth:`~rolex.Rolex.rnd_datetime()` has similar API


Time Series
-----------
Generate a time series is simple::
	
	>>> start = "2014-01-01 03:00:00"
	>>> end = "2014-01-01 03:10:00"
	>>> rolex.time_series(start=start, end=end, freq="5min")
	[datetime.datetime(2014, 1, 1, 3, 0),
	 datetime.datetime(2014, 1, 1, 3, 5),
	 datetime.datetime(2014, 1, 1, 3, 10)]

If you want it repeat specified times from start point, do this::

	>>> start = "2014-01-01 03:00:00"
	>>> rolex.time_series(start=start, periods=3, freq="5min")
	[datetime.datetime(2014, 1, 1, 3, 0),
	 datetime.datetime(2014, 1, 1, 3, 5),
	 datetime.datetime(2014, 1, 1, 3, 10)]

And it has :meth:`more options <rolex.Rolex.time_series>` available.


:meth:`rolex.Rolex.weekday_series()`` helps you create a time series only on specifid weekday::
	
	>>> start = "2014-01-01 06:30:25"
	>>> end = "2014-02-01 06:30:25"
	>>> rolex.weekday_series(start, end, weekday=2) # all tuesday
	[datetime.datetime(2014, 1, 7, 6, 30, 25),
	 datetime.datetime(2014, 1, 14, 6, 30, 25),
	 datetime.datetime(2014, 1, 21, 6, 30, 25),
	 datetime.datetime(2014, 1, 28, 6, 30, 25)]


Time Delta
----------
The method name described itself.

- :meth:`rolex.Rolex.add_seconds()`
- :meth:`rolex.Rolex.add_minutes()`
- :meth:`rolex.Rolex.add_hours()`
- :meth:`rolex.Rolex.add_days()`
- :meth:`rolex.Rolex.add_weeks()`
- :meth:`rolex.Rolex.add_months()`
- :meth:`rolex.Rolex.add_years()`


Playing with SQL
----------------
You man have this demands while playing with SQL database. select data within one day, one month, or one year. Basically you gonna do::

	select * from table_name where datetime_column between '2014-01-01 00:00:00' to '2014-01-01 23:59:59'

``rolex`` can help::

	>>> rolex.day_interval(2014, 1, 1)
	(datetime.datetime(2014, 1, 1, 0, 0),
 	 datetime.datetime(2014, 1, 1, 23, 59, 59))

	>>> rolex.month_interval(2014, 6)
	(datetime.datetime(2014, 6, 1, 0, 0),
 	 datetime.datetime(2014, 6, 30, 23, 59, 59))

 	>>> rolex.year_interval(2014)
 	(datetime.datetime(2014, 1, 1, 0, 0),
 	 datetime.datetime(2014, 12, 31, 23, 59, 59))


If you got an idea, or have request for more utility method, tell me at here https://github.com/MacHu-GWU/rolex-project/issues