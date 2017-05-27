#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import create_table
from utils.scraping import Spider

db_path = "~/.sqlite"

cols = ["sent", "polarity", "subjectivity", "url"]

starting_point = 'https://en.wikipedia.org/wiki/Donald_Trump'

spider = Spider(1000, 'Trump')

rows = spider.scrape(starting_point)

rows = spider.results

create_table(rows, 'trump', db_path, cols, delete_existing=True)
