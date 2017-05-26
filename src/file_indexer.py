#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO
#

import os
import itertools
from functools import reduce
import operator
from insertion import connect, close_connection, drop_table

raw = os.walk(os.path.expanduser('~'))

# lists
data = itertools.starmap(lambda dirpath, dirnames, filenames: [dirpath] + [os.path.join(dirpath, f) for f in filenames], raw)

# flattened to 1 level
data = reduce(operator.add, data)

# filtered to files
data = filter(os.path.isfile, data)

# stats
data = map(lambda node: tuple([node]) + os.stat(node), data)

connection, cursor, query = connect("~/.sqlite")

drop_table('nodes', cursor)

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

for i in data:
    query('INSERT INTO nodes VALUES {}'.format(i))

assert close_connection(connection)



