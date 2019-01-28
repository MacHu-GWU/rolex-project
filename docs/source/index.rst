Release v\ |release| (:ref:`What's new? <release_history>`).


.. include:: ../../README.rst


Usage
------------------------------------------------------------------------------

First, let's import::

    import rolex
    from datetime import datetime, date


Parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parse anything to ``datetime``:

.. code-block:: python

    # parse string
    >>> rolex.parse_datetime("2014-01-15T17:58:31Z-0400")
    datetime.datetime(2014, 1, 15, 17, 58, 31, tzinfo=datetime.timezone(datetime.timedelta(-1, 72000)))

    # parse numbers by mean of timestamps from epoch
    >>> rolex.parse_datetime(1234567890)
    datetime.datetime(2009, 2, 13, 23, 31, 30)

    # convert date to datetime
    >>> rolex.parse_datetime(date(2015, 12, 24))
    datetime.datetime(2015, 12, 24, 0, 0)

    # remains datetime
    >>> rolex.parse_datetime(datetime(2015, 11, 24, 20, 30))
    datetime.datetime(2015, 11, 24, 20, 30)

Also works fine with ``date``::

    # parse string
    >>> rolex.parse_date("Saturday, September 20, 2014")
    datetime.date(2014, 9, 20)

    # parse numbers by mean of days from ordinary 0000-01-01
    >>> rolex.parse_date(720000)
    datetime.date(1972, 4, 17)

    ...

If rolex meets a unknown time format, automatically, it will start using `dateutil <https://dateutil.readthedocs.io/en/stable/>`_. So if rolex CAN NOT parse the string, then dateutil can't either. **But rolex's built in method is 4x times faster** than ``dateutil`` for known format. If ``rolex`` failed to parse your string, **please submit it to** https://github.com/MacHu-GWU/rolex-project/issues.


Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Python2 doesn't implement ``datetime.timestamp()``. And in Python3, it assume that it's a local time by default, for example::

    >>> datetime(1970, 1, 1).timestamp() # In Python3
    18000 # New York Time Zone, it should be zero

**That's not good**!

``rolex`` provide more flexibility:

- :meth:`~rolex.util.to_utctimestamp()`: assume it's utc time if it is a naive datetime
- :meth:`~rolex.util.from_utctimestamp()`: return a local time represent of a utc timestamp

See also: :meth:`~rolex.util.to_ordinal()`, :meth:`~rolex.util.from_ordinal()`.


Random Generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:meth:`~rolex.generator.rnd_date()`, :meth:`~rolex.generator.rnd_datetime()`:

    # random date from 1970-01-01 to today
    >>> rolex.rnd_date()
    datetime.date(1994, 10, 13)

    # random datetime from 1970-01-01 00:00:00 to now
    >>> rolex.rnd_datetime()
    datetime.datetime(2011,

    # random date / datetime between:
    >>> rolex.rnd_date("2015-01-01", "2015-12-31") # or rnd_datetime
    datetime.date(2015, 5, 14)

:meth:`~rolex.generator.rnd_date_array()`, :meth:`~rolex.generator.rnd_datetime_array()`

    # gives you length-6 date list
    >>> rolex.rnd_date_array(6, "2015-01-01", "2015-12-31") # or rnd_datetime_array

    # gives you 2 x 3 date matrix
    >>> rolex.rnd_date_array((2, 3), "2015-01-01", "2015-12-31") # or rnd_datetime_array


Time Series
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate a time series is simple:

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

And it has :meth:`more options <rolex.generator.time_series>` available.


:meth:`~rolex.generator.weekday_series()` helps you create a time series only on specifid weekday::

    >>> start = "2014-01-01 06:30:25"
    >>> end = "2014-02-01 06:30:25"
    >>> rolex.weekday_series(start, end, weekday=2) # all tuesday
    [datetime.datetime(2014, 1, 7, 6, 30, 25),
     datetime.datetime(2014, 1, 14, 6, 30, 25),
     datetime.datetime(2014, 1, 21, 6, 30, 25),
     datetime.datetime(2014, 1, 28, 6, 30, 25)]


Time Delta
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The method name described itself.

- :meth:`~rolex.math.add_seconds()`
- :meth:`~rolex.math.add_minutes()`
- :meth:`~rolex.math.add_hours()`
- :meth:`~rolex.math.add_days()`
- :meth:`~rolex.math.add_weeks()`
- :meth:`~rolex.math.add_months()`
- :meth:`~rolex.math.add_years()`

Example::

    >>> rolex.add_seconds("2015-01-01", 3600 * 24)
    datetime.datetime(2015, 1, 2, 0, 0, 0)


Timezone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- :meth:`~rolex.util.to_utc(a_datetime)`: Convert a time awared datetime to utc datetime.
- :meth:`~rolex.util.utc_to_tz()`: Convert a UTC datetime to a time awared local time
- :meth:`~rolex.util.utc_to_local()`: Convert a UTC datetime to current machine local timezone datetime.


Playing with SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


.. include:: ../../AUTHORS.rst


API Document
------------------------------------------------------------------------------

* :ref:`by Name <genindex>`
* :ref:`by Structure <modindex>`
