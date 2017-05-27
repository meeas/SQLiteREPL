#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from typing import Tuple, List
from textblob import TextBlob

Entry = Tuple[str, float, float, str]

class Spider():
    def __init__(self, max_entries: int, theme: str):
        self._max = max_entries
        self._rows = []
        self._theme = theme


    def scrape(self, starting_point: str):
        focus = starting_point
        html = urlopen(focus).read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        blob = TextBlob(text)
        for sent in blob.sentences:
            if self._theme in sent:
                self._add_entry(str(sent), sent.polarity, sent.subjectivity, focus)

        if text.count(self._theme) >= 3 and len(self._rows) < self._max:
            anchors = soup.find_all('a', limit=5)
            links = [anchor['href'] for anchor in anchors]
            for url in links:
                try:
                    self.scrape(url)
                except ValueError:
                    pass


    @property
    def results(self) -> List[Entry]:
        return self._rows


    def _add_entry(self, sent: str, polarity: float, subjectivity: float, URL: str):
        self._rows.append(tuple([sent, polarity, subjectivity, URL]))

spider = Spider(30, 'trump')
spider.scrape('https://www.theguardian.com/us-news/2017/may/27/donald-trumps-europe-tour-leaves-leaders-shaken')
