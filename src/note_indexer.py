#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import glob
from re import compile
from collections import Counter
from db import drop_table, create_table

notes_dir = os.path.expanduser("~/vimwiki")

db_path = '~/.sqlite'

drop_table(db_path ,'notes')

cols = ["name", "mode", "inode", "device", "nlinks", "uid", "gid", "size", "atime", "mtime", "ctime", 'text']

word_counter = Counter()

filtered = filter(os.path.isfile ,glob.iglob(os.path.join(notes_dir ,"**"), recursive=True))

filtered = filter(compile("((wiki)|(md)|(rst))$").search, filtered)

rows = list(map(lambda f: tuple([f]) + os.stat(f) + tuple([open(f).read()]) ,filtered))

create_table(rows, 'notes', db_path, cols)
