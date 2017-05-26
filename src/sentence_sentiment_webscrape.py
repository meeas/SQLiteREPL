#!/usr/bin/env python
# -*- coding: utf-8 -*-

from textblob import TextBlob
from pandas import DataFrame
import pandas
from urllib.request import urlopen
from bs4 import BeautifulSoup

# pandas.reset_option('expand_frame_repr')
# pandas.set_option('max_colwidth', 10)

pandas.set_option('max_rows', 9999)

text_holder = ""

websites = [
    "http://pandas.pydata.org/pandas-docs/version/0.18.1/generated/pandas.DataFrame.sort_values.html#pandas.DataFrame.sort_values",
    "https://docs.python.org/3/library/urllib.request.html#module-urllib.request"
    "https://stackoverflow.com/questions/24988873/python-sort-descending-dataframe-with-pandas",
    "https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sort_values.html",
    "https://www.quora.com/When-is-better-to-use-NLTK-vs-Sklearn-vs-Gensim"
]

for site in websites:
    try:
        html = urlopen(site).read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        text_holder += text
    except UnicodeDecodeError:
        pass

blob = TextBlob(text_holder)

sentences = blob.sentences

tupled = [(str(sent), sent.subjectivity, sent.polarity)  for sent in sentences]

df = DataFrame(tupled, columns=['sentence', 'subjectivity', 'polarity'])

print(df)
