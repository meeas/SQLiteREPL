#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, Tag
from urllib.request import urlopen
from typing import Tuple, List, Iterator
from textblob import TextBlob
import re
from re import compile
from urllib.error import HTTPError, URLError
from http.client import RemoteDisconnected
import logging
from queue import Queue

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s : %(asctime)s : %(lineno)s : %(message)s.',
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
        l.info('Filtering links that end with ".zip" or ".rar"')
        l.info('Filtering links through Django regex')
        if regex.search(URL) and not compile('(\.((zip)|(rar)|(pdf)|(docx)))$').search(URL):
            return True
        return False

    def depth_first_scrape(self, starting_point: str):
        if len(self._rows) > self._max:
            l.info('max is {} and there is {} entries. Returning'.format(self._max, len(self._rows)))
            return
        focus_url = starting_point
        l.info('Focus URL: {}'.format(focus_url))
        l.info('Length of rows is {}'.format(len(self._rows)))
        l.info('Traversed URLs: {}'.format(self._traversed))
        l.info('Traversed {} URLs'.format(len(self._traversed)))
        try:
            html = urlopen(focus_url).read()
        except (HTTPError,URLError):
            l.debug('HTTPError or URLError occured when trying to request the html')
            return
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        l.info('Filtering too long sentences')
        l.info('Looping through sentences, checking if they contain "{}"'.format(self._theme))

        self._add_entries(text, focus_url)

        matches = text.count(self._theme)

        l.info('found {} matches in the content of {}'.format(matches, focus_url))

        if matches > 10 and len(self._rows) < self._max:
            links = self._generate_links(soup)
            links = filter(lambda link: link not in self._traversed, links)
            for url in links:
                l.info('Appending {} to self._traversed'.format(focus_url))
                self._traversed.append(url)
                l.info('About to recurse by passing {}'.format(url))
                self.depth_first_scrape(url)
        l.info('End of function reached, returning')
        return

    def _generate_links(self, soup: BeautifulSoup) -> Iterator[Tag]:
        anchors = soup.find_all('a')
        l.info('Parsed {} anchor tags'.format(len(anchors)))
        links = []
        for i in range(len(anchors)):
            try:
                if self._theme in anchors[i].get_text() or \
                        self._theme in anchors[i].parent.get_text() or \
                        self._theme in anchors[i].parent.parent.get_text() or \
                        self._theme in anchors[i].parent.parent.parent.get_text():
                    links.append(anchors[i]['href'])
            except (KeyError,ValueError,AttributeError):
                l.debug('KeyError or ValueError occured when trying to access the href attribute')
                l.debug('Most likely there was no href attribute with a valid URL')
        l.info('Filtering links using Django regexp and removing those already traversed')
        links = filter(lambda link: Spider.validate_url(link), links)
        return links

    def breadth_first_scrape(self, starting_point: str):

        # initialise
        to_be_scraped = Queue()

        # put the firs (starting URL)
        to_be_scraped.put(starting_point)

        # loop until the queue is empty
        while not to_be_scraped.empty() and len(self._rows) < self._max:

            # l.info('The queue of items to be scraped: {}'.format(list(to_be_scraped)))

            l.info('Length of rows is {}'.format(len(self._rows)))

            l.info('Length of queue of items to be scraped: {}'.format(to_be_scraped.qsize()))

            focus_url = to_be_scraped.get()

            l.info('Focus URL: {}'.format(focus_url))

            try:
                html = urlopen(focus_url).read()

            except (HTTPError,URLError,RemoteDisconnected):
                l.debug('HTTPError or URLError or RemoteDisconnected occured when trying to request the html')
                continue

            soup = BeautifulSoup(html, 'html.parser')

            text = soup.get_text()

            self._add_entries(text, focus_url)

            # fetch all soup tags
            soup_a_tags = soup.find_all('a')

            l.info('Parsed {} anchor tags'.format(len(soup_a_tags)))

            # initialise
            links = []

            # iterate over soup tags
            links = self._generate_links(soup)

            # count matches on the focus page
            matches = text.count(self._theme)

            l.info('found {} matches in the content of {}'.format(matches, focus_url))


            # populate the queue
            # add to queue if less than max
            for link in links:
                if len(self._rows) < self._max and matches >= 2:
                    l.info('Appending {} to to_be_scraped'.format(link))
                    to_be_scraped.put(link)

            l.info('End of this loop, continuing')

    @property
    def results(self) -> List[Entry]:
        return self._rows

    def _add_entry(self, sent: str, polarity: float, subjectivity: float, URL: str):
        self._rows.append(tuple([sent, polarity, subjectivity, URL]))

    def _add_entries(self, text: str, focus_url: str):

        blob = TextBlob(text)

        sentences = filter(lambda sent: len(sent) < 1500, blob.sentences)

        for sent in sentences:

            if re.compile(".*" + self._theme.lower() + ".*", flags=re.IGNORECASE).search(str(sent)):

                l.info('Adding an entry to self._rows')

                self._add_entry(Sanitizer(sent.string).sanitize(), sent.polarity,
                                sent.subjectivity, focus_url)
