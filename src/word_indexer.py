#!/usr/bin/env python
# -*- coding: utf-8 -*-


### the logic

# connect to the database,
# remove the table in case it exists
# create (or replace the old table) a new table
# every row is (word: str, frequency: int, tag: str)
# list of these rows will be inserted into db by iteration

import os
import sys

# db
import sqlite3

# list files
import glob

# remove punctuation
from re import compile
from collections import Counter

# lexical analysys
from textblob import TextBlob

# typing
from typing import Tuple, Iterator, Generator

# define types
Dir = str
File = str
Word = str
Tag = str
Frequency = int
Row = Tuple[Word, Frequency, Tag]

#### BEGIN ####

# sqlite connect

def gen_files(starting_point: Dir) -> Iterator[File]:
    # make recursive, use iglob for efficiency
    filtered = filter(os.path.isfile, glob.iglob(
        os.path.join(starting_point, "**"), recursive=True))

    # looks in files with .md .rst or .wiki extension
    filtered = filter(compile("(\.(wiki)|(md)|(rst)|(txt))$").search, filtered)

    return filtered

# every row is (word: str, frequency: int, tag: str)


def gen_rows() -> Generator[Row, None , None]:


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

db_path = "~/.sqlite"

query = connect(db_path)

# iterate through files

for row in gen_rows():
    query("INSERT INTO words VALUES (?, ?, ?)", row)

