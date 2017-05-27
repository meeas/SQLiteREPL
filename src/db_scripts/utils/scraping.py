#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from typing import Tuple, List
from textblob import TextBlob
import re
from re import compile
from urllib.error import HTTPError, URLError
from itertools import filterfalse
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: [%(asctime)s] [%(lineno)s] %(message)s.',
    datefmt="%I:%M:%S")

l = logging.getLogger()

Entry = Tuple[str, float, float, str]

punctuation = "£%$![]{}~#-+=>^&*`¬</"

regex = compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class Sanitizer():
    def __init__(self, text: str):
        self._text = text

    def _remove_punct(self):
        translator = str.maketrans(self._text, self._text, "£%$!()[]{}~#-+=>^&*`¬</")
        self._text.translate(translator)

    def _remove_references(self):
        self._text = compile("\[\d+\]+").sub("", self._text)

    def _beautify(self):
        self._text = compile("[\n\t ]{2,}").sub(" ", self._text)

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
        l.info('Spider created')
        l.info("max set to {}".format(max_entries))
        l.info("theme set to {}".format(theme))

    def validate_url(URL: str) -> bool:
        if regex.search(URL):
            return True
        return False

    def scrape(self, starting_point: str):
        if len(self._rows) > self._max:
            l.info('max is {} and there is {} entries. Returning'.format(self._max, len(self._rows)))
            return
        focus = starting_point
        l.info('focus is ' + focus)
        l.info('Length of rows is {}'.format(len(self._rows)))
        l.info('Traversed URLs: {}'.format(self._traversed))
        l.info('Traversed {} URLs'.format(len(self._traversed)))
        try:
            html = urlopen(focus).read()
        except (HTTPError,URLError):
            l.debug('HTTPError or URLError occured when trying to request the html')
            return
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        blob = TextBlob(text)
        l.info('Filtering too long sentences')
        sentences = filter(lambda sent: len(sent) < 1500, blob.sentences)
        l.info('Looping through sentences, checking if they contain {}'.format(self._theme))
        for sent in sentences:

            if self._theme.lower() in sent.lower():

                l.info('Adding an entry to self._rows')

                self._add_entry(Sanitizer(sent.string).sanitize(), sent.polarity,
                                sent.subjectivity, focus)

        matches = text.count(self._theme)

        l.info('found {} matches in the content of {}'.format(matches, focus))

        if matches > 5 and len(self._rows) < self._max:
            anchors = soup.find_all('a')
            l.info('Parsed {} anchor tags'.format(len(anchors)))
            links = []
            for i in range(len(anchors)):
                try:
                    anchor_text = anchors[i].get_text()
                    if self._theme in anchor_text or \
                            self._theme in anchors[i].parent.get_text() or \
                            self._theme in anchors[i].parent.parent.get_text() or \
                            self._theme in anchors[i].parent.parent.parent.get_text():
                        links.append(anchors[i]['href'])
                except (KeyError,ValueError):
                    l.debug('KeyError or ValueError occured when trying to access the href attribute')
            l.info('Filtering links using Django regexp and removing those already traversed')
            links = filter(lambda link: link not in self._traversed and Spider.validate_url(link), links)
            l.info('Filtering links that end with ".zip" or ".rar"')
            links = filterfalse(compile('(\.((zip)|(rar)|(pdf)|(docx)))$').search, links)
            for url in links:
                l.info('Appending {} to self._traversed'.format(focus))
                self._traversed.append(url)
                l.info('About to recurse by passing {}'.format(url))
                self.scrape(url)
        l.info('End of function reached, returning')
        return

    @property
    def results(self) -> List[Entry]:
        return self._rows

    def _add_entry(self, sent: str, polarity: float, subjectivity: float, URL: str):
        self._rows.append(tuple([sent, polarity, subjectivity, URL]))
