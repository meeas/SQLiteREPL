#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# db
import sqlite3
from db import connect, create_table, close_connection, drop_table

# list files
from glob import iglob

# remove punctuation
from re import compile
from collections import Counter

# lexical analysys
from textblob import TextBlob

db_path = "~/.sqlite"

# sqlite connect

filtered = filter(os.path.isfile, glob.iglob(os.path.join(starting_point, "**"), recursive=True))

# looks in files with .md .rst or .wiki extension
filtered = filter(compile("(\.(wiki)|(md)|(rst)|(txt))$").search, filtered)

# every row is (word: str, frequency: int, tag: str)

text = str()

for f in gen_files(starting_dir):
    text += open(f, encoding="utf-8").read()

# it's a property
blob =  TextBlob(text)

words = blob.words

tags = blob.tags

# only tag words, leave out punctuation
# [(word, tag), (word, tag), ...]

tags = filter(lambda two_tup: two_tup[0] in words , tags)

tags = dict(tags)

# dict such that { <word: str, freq: int>, ... }
word_counter = Counter(blob.words)

for word in word_counter:
    try:
        yield (word, word_counter[word], tags[word])
    except KeyError:
        pass

# now we have an iterator of tuples such that
# tuple(word, tag)

# we still don't have frequency

# initialise variables
starting_dir = os.path.expanduser("~/vimwiki")

# iterate through files
