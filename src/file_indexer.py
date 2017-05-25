#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO
#

import os
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

try:
    query("DROP TABLE nodes")
    print("Existing nodes table deleted")
except:
    pass

query("CREATE TABLE nodes( \
        name TEXT NOT NULL PRIMARY KEY, \
        mode INTEGER, \
        inode INTEGER, \
        device INTEGER, \
        nlinks INTEGER, \
        uid INTEGER, \
        gid INTEGER, \
        size INTEGER, \
        atime INTEGER, \
        mtime INTEGER, \
        ctime INTEGER \
        )")

for i in details:
    query("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", i)

conn.commit()
curr.close()
conn.close()

