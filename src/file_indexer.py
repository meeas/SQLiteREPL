#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO
#

import os
from typing import Any, List, Set, Dict, Iterator, Iterable
import itertools
from functools import reduce
import sqlite3
import operator

raw = os.walk(os.path.expanduser('~'))

lists = itertools.starmap(lambda dirpath, dirnames, filenames: [dirpath] + [os.path.join(dirpath, f) for f in filenames], raw)

flattened = reduce(operator.add, lists)

flattened = filter(os.path.isfile, flattened)

details = map(lambda node: tuple([node]) + tuple(os.stat(node)), flattened)

db_path = os.path.expanduser("~/.sqlite")
conn = sqlite3.connect(db_path)
curr = conn.cursor()
query = curr.execute

for i in details:
    query("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", i)

conn.commit()
curr.close()
conn.close()

