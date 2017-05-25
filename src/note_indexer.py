#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sqlite3
import glob
from re import findall, compile
from collections import Counter

db_path = os.path.expanduser("~/.sqlite")
conn = sqlite3.connect(db_path)
curr = conn.cursor()
query = curr.execute
notes_dir = os.path.expanduser("~/vimwiki")

try:
    query("DROP TABLE notes")
    print("Existing notes table deleted")
except:
    pass

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
