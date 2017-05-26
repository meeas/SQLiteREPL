#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from glob import iglob
from textblob import TextBlob
from pandas import DataFrame
import pandas

# pandas.reset_option('expand_frame_repr')
# pandas.set_option('max_colwidth', 120)
pandas.set_option('max_rows', 9999)

starting_point = os.curdir

starting_point = os.path.join(starting_point, '**')

text_holder = ""

files = filter(os.path.isfile, iglob(starting_point))

for node in files:
    try:
        text_holder += open(node).read()
    except UnicodeDecodeError:
        pass

blob = TextBlob(text_holder)

word_counter = blob.word_counts

tupled = [(i, word_counter[i]) for i in word_counter if len(i) >= 3 and i.isalpha()]

df = DataFrame(tupled, columns=['word', 'frequency']).sort_values('frequency', ascending=False)

print(df)
