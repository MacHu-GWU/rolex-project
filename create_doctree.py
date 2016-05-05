#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from docfly import Docfly
import shutil
 
try:
    shutil.rmtree(r"source\rolex")
except Exception as e:
    print(e)
     
docfly = Docfly("rolex", dst="source", 
    ignore=[
        "rolex.zzz_manual_install.py",
        "rolex.six.py",
        "rolex.template.py",
        "rolex.tests",
    ]
)
docfly.fly()
