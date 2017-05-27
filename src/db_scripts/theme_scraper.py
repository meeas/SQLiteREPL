#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import create_table
from utils.scraping import Spider

db_path = "~/.sqlite"

cols = ["sent", "polarity", "subjectivity", "url"]

starting_point = 'https://en.wikipedia.org/wiki/Compiler'

spider = Spider(300, 'lang')

rows = spider.scrape(starting_point)

rows = spider.results

create_table(rows, 'compiler', db_path, cols, delete_existing=True)
