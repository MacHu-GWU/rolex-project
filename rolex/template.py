#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date, DateTime string template.

Reference: https://msdn.microsoft.com/en-us/library/hc4ky857.aspx
"""

DateTemplatesAndExample = [
    # Dash delimiter
    ("%Y-%m-%d",    "2014-09-20"),
    ("%m-%d-%Y",    "09-20-2014"),
    
    # Slash delimiter
    ("%Y/%m/%d",    "2014/09/20"),
    ("%m/%d/%Y",    "09/20/2014"),
    
    # Dot delimiter
    ("%Y.%m.%d",    "2014.09.20"),
    ("%m.%d.%Y",    "9.20.2014"),
    
    # Long Date Pattern
    ("%B %d, %Y",       "September 20, 2014"),
    ("%A, %B %d, %Y",   "Saturday, September 20, 2014"),
    ("%b %d, %Y",       "Sep 20, 2014"),
    ("%a, %b %d, %Y",   "Sat, Sep 20, 2014"),
    
    # No delimiter
    ("%Y%m%d",      "20140920"),
    ("%y%m%d",      "140920"),
    ("%m%d%Y",      "09202014"),
    ("%m%d%y",      "092014"),
]
DateTemplates = [tpl for tpl, example in DateTemplatesAndExample]

DatetimeTemplatesAndExample = [
    # Dash delimiter
    ("%Y-%m-%d %H:%M:%S",        "2014-01-15 17:58:31"),
    ("%Y-%m-%d %H:%M:%S.%f",     "2014-01-15 17:58:31.1234"),
    ("%Y-%m-%d %H:%M",           "2014-01-15 17:58"),
    ("%Y-%m-%d %I:%M:%S %p",     "2014-01-15 5:58:31 PM"),
    ("%Y-%m-%d %I:%M %p",        "2014-01-15 05:58 PM"),
    ("%Y-%m-%d %I %p",           "2014-01-15 05 PM"),
    
    # Dash delimiter
    ("%m-%d-%Y %H:%M:%S",        "1-15-2014 17:58:31"),
    ("%m-%d-%Y %H:%M:%S.%f",     "1-15-2014 17:58:31.1234"),
    ("%m-%d-%Y %H:%M",           "1-15-2014 17:58"),
    ("%m-%d-%Y %I:%M:%S %p",     "1-15-2014 5:58:31 PM"),
    ("%m-%d-%Y %I:%M %p",        "1-15-2014 05:58 PM"),
    ("%m-%d-%Y %I %p",           "1-15-2014 05 PM"),
    
    # Slash delimiter
    ("%Y/%m/%d %H:%M:%S",        "2014/01/15 17:58:31"),
    ("%Y/%m/%d %H:%M:%S.%f",     "2014/01/15 17:58:31.1234"),
    ("%Y/%m/%d %H:%M",           "2014/01/15 17:58"),
    ("%Y/%m/%d %I:%M:%S %p",     "2014/01/15 5:58:31 PM"),
    ("%Y/%m/%d %I:%M %p",        "2014/01/15 05:58 PM"),
    ("%Y/%m/%d %I %p",           "2014/01/15 05 PM"),

    # Slash delimiter
    ("%m/%d/%Y %H:%M:%S",        "1/15/2014 17:58:31"),
    ("%m/%d/%Y %H:%M:%S.%f",     "1/15/2014 17:58:31.1234"),
    ("%m/%d/%Y %H:%M",           "1/15/2014 17:58"),
    ("%m/%d/%Y %I:%M:%S %p",     "1/15/2014 5:58:31 PM"),
    ("%m/%d/%Y %I:%M %p",        "1/15/2014 05:58 PM"),
    ("%m/%d/%Y %I %p",           "1/15/2014 05 PM"),
    
    ("%H:%M:%S %m/%d/%Y",        "17:58:31 1/15/2014"),
    ("%H:%M:%S.%f %m/%d/%Y",     "17:58:31.1234 1/15/2014"),
    ("%H:%M %m/%d/%Y",           "17:58 1/15/2014"),
    ("%I:%M:%S %p %m/%d/%Y",     "5:58:31 PM 1/15/2014"),
    ("%I:%M %p %m/%d/%Y",        "05:58 PM 1/15/2014"),
    ("%I %p %m/%d/%Y",           "05 PM 1/15/2014"),
    
    # No delimiter
    ("%Y%m%d%H",                 "2014011506"),
    ("%Y%m%d%H%M",               "201401150630"),
    ("%Y%m%d%H%M%S",             "20140115063015"),
    ("%Y%m%d%H%M%S.%f",          "20140115063015.123"),
    
    # No delimiter
    ("%y%m%d%H",                 "14011506"),
    ("%y%m%d%H%M",               "1401150630"),
    ("%y%m%d%H%M%S",             "140115063015"),
    ("%y%m%d%H%M%S.%f",          "140115063015.123"),

    # ISO 8601
    ("%Y-%m-%dT%H:%M:%S",        "2014-01-15T17:58:31"),
    ("%Y-%m-%dT%H:%M:%S.%f",     "2014-01-15T17:58:31.1234"),
    ("%Y-%m-%dT%H:%M:%SZ%z",     "2014-01-15T17:58:31Z-0400"),
    ("%Y-%m-%dT%H:%M:%SZ%Z",     "2014-01-15T17:58:31ZUTC"),
    ("%Y-%m-%dT%H:%M:%S.%fZ%z",  "2014-01-15T17:58:31.1234Z-0400"),
    ("%Y-%m-%dT%H:%M:%S.%fZ%Z",  "2014-01-15T17:58:31.1234ZUTC"),
    
    # RCF1123
    ("%a, %d %b %Y %H:%M:%S GMT", "Wed, 15 Jan 2014 17:58:31 GMT")
]
DatetimeTemplatesAndExample = DatetimeTemplatesAndExample + DateTemplatesAndExample
DatetimeTemplates = [tpl for tpl, example in DatetimeTemplatesAndExample]


#--- Unittest ---
if __name__ == "__main__":
    import unittest
    from datetime import datetime, date
    
    class Unittest(unittest.TestCase):
        def test_all(self):
            for tpl, example in DateTemplatesAndExample:
                d1 = datetime.strptime(example, tpl).date()
                
            for tpl, example in DatetimeTemplatesAndExample:
                dt1 = datetime.strptime(example, tpl)
                 
    unittest.main()