#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import create_table
from utils.scraping import Spider

db_path = "~/.sqlite"

cols = ["sent", "polarity", "subjectivity", "url"]

starting_point = 'https://en.wikipedia.org/wiki/Linux'

spider = Spider(2000, 'linux')

rows = spider.breadth_first_scrape(starting_point)

rows = spider.results

create_table(rows, 'linux', db_path, cols, delete_existing=True)
