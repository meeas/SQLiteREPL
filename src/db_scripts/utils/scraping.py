#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from typing import Tuple, List
from textblob import TextBlob
from re import compile

Entry = Tuple[str, float, float, str]

punctuation = "£%$![]{}~#-+=>^&*`¬</"

class Sanitizer():
    def __init__(self, text: str):
        self._text = text

    def _remove_punct(self):
        translator = str.maketrans(self._text, self._text, "£%$!()[]{}~#-+=>^&*`¬</")
        self._text.translate(translator)

    def _remove_references(self):
        self._text = compile("\[\d+\]+").sub("", self._text)

    def _beautify(self):
        self._text.replace("\n", " ")
        self._text.replace("\t", " ")
        self._text = compile(" {2,}").sub(" ", self._text)

    def sanitize(self):
        self._beautify()
        self._remove_punct()
        self._remove_references()
        return self._text


class Spider():
    def __init__(self, max_entries: int, theme: str):
        self._max = max_entries
        self._rows = []
        self._theme = theme
        self._traversed = []

    def scrape(self, starting_point: str):
        focus = starting_point
        html = urlopen(focus).read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        blob = TextBlob(text)
        sentences = filter(lambda sent: len(sent) < 1500, blob.sentences)
        for sent in sentences:

            if self._theme.lower() in sent.lower():

                self._add_entry(Sanitizer(sent.string).sanitize(), sent.polarity,
                                sent.subjectivity, focus)

        if text.count(self._theme) >= 7 and len(self._rows) < self._max:
            anchors = soup.find_all('a')
            links = []
            for i in range(len(anchors)):
                try:
                    links.append(anchors[i]['href'])
                    # links = [anchor['href'] for anchor in anchors]
                except KeyError:
                    pass
            links = filter(compile('^(https?)').search, links)
            links = filter(lambda link: link not in self._traversed, links)
            for url in links:
                self._traversed.append(url)
                try:
                    return self.scrape(url)
                except ValueError:
                    pass
        return

    @property
    def results(self) -> List[Entry]:
        return self._rows

    def _add_entry(self, sent: str, polarity: float, subjectivity: float, URL: str):
        self._rows.append(tuple([sent, polarity, subjectivity, URL]))
