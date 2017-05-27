#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
import typing
from typing import Tuple
from textblob import TextBlob

Entry = Tuple[str, float, float, str]

class Spider():
    def __init__(self, max_links: int, theme: str):
        __start = starting_point
        __max = max_links
        __rows = []
        __theme = theme
        while len(__rows) > __max:
            scrape()


    def scrape(self, starting_point: str):
        focus = starting_point
        html = urlopen(focus).read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        blob = TextBlob(text)
        for sent in blob.sentences:
            if self.__theme in sent:
                self._add_entry(str(sent), sent.polarity, sent.subjectivity, focus)

        if text.count(self.__theme) >= 3 and len(self.__rows) > self.__max:
            anchors = soup.find_all('a', limit=5)
            links = [anchor['href'] for anchor in anchors]
            for url in links:
                scrape(url)

    def results(self) -> List[Entry]:
        return self.__rows

    def _add_entry(self, sent: str, polarity: float, subjectivity: float, URL: str) -> Entry:
        __rows.append(tuple(sent, polarity, subjectivity, URL))
