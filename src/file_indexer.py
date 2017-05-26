#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AIM: index the whole file system starting from 'starting_location'
# Row[name, mode, inode, device, nlinks, uid, gid, size, atime, mtime, ctime]

import os
from itertools import starmap
from functools import reduce
import operator
from db import drop_table, connect, close_connection
from pandas import DataFrame

db_path = "~/.sqlite"
starting_location = '~'
cols = ["name", "mode", "inode", "device", "nlinks", "uid", "gid", "size", "atime", "mtime", "ctime"]

# necessary as DataFrames print in the reverse order
cols.reverse()

connection, cursor, query = connect(db_path)

raw = os.walk(os.path.expanduser(starting_location))

# lists
data = starmap(lambda dirpath, dirnames, filenames: [dirpath] + [os.path.join(dirpath, f) for f in filenames], raw)

# flattened to 1 level
data = reduce(operator.add, data)

# filtered to files
data = filter(os.path.isfile, data)

# stats
data = list(map(lambda f : os.stat(f) + tuple([f]), data))

drop_table(db_path, 'files')

df = DataFrame(data, columns=cols)

df.to_sql(con=connection, name="files")

close_connection(connection)
