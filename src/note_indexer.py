#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import glob
from re import findall, compile
from collections import Counter
from db import quick_query, drop_table

drop_table('notes')

query("CREATE TABLE notes ( \
      name TEXT, \
      size INTEGER, \
      atime INTEGER, \
      mtime INTEGER, \
      ctime INTEGER \
)")

word_counter = Counter()

filtered = filter(os.path.isfile ,glob.iglob(os.path.join(notes_dir ,"**"), recursive=True))

filtered = filter(compile("((wiki)|(md)|(rst))$").search, filtered)

for f in filtered:
    text = open(f, 'r').read()
    word_list = findall("\w{3,}", text)
    word_counter.update(word_list)

print(word_counter)

