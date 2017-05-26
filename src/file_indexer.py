#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import itertools
from functools import reduce
import operator
from insertion import drop_table, insert_rows, quick_query

raw = os.walk(os.path.expanduser('~'))

db_path = "~/.sqlite"

# lists
data = itertools.starmap(lambda dirpath, dirnames, filenames: [dirpath] + [os.path.join(dirpath, f) for f in filenames], raw)

# flattened to 1 level
data = reduce(operator.add, data)

# filtered to files
data = filter(os.path.isfile, data)

# stats
data = map(lambda node: tuple([node]) + os.stat(node), data)

drop_table(db_path, 'nodes')

quick_query(db_path, "CREATE TABLE nodes( \
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

insert_rows(data, "nodes", db_path)
