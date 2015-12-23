# -*- coding: utf-8 -*-

import os
import re
import urllib2
from bs4 import BeautifulSoup

class YNUCalendar:
    _CALENDER_URL = 'http://www.ynu.ac.jp/campus/schedule/year.html'
    def __init__(self):
        raw_html = self._fetch_raw_html()
        self._raw_html = raw_html
        self._bs_html = BeautifulSoup(raw_html, "lxml")
        self._bs_inner = self._bs_html.find(id="contentInner")
        pass

    def _fetch_raw_html(self):
        connection = urllib2.urlopen(self._CALENDER_URL)
        raw_html = connection.read()
        connection.close()
        return raw_html

    def get_year_num(self):
        text = self._bs_inner.h2.get_text()
        return re.search("\d+", text).group(0)

    def get_events(self):
        events = []
        for tr in self._bs_inner.find_all("tr"):
            td = tr.find_all("td")
            events.append({"name": td[0].get_text(), "term": re.sub("[\n\r\t ]", "", td[1].get_text())})
        return events

if __name__ == '__main__':
    #pass
    parser = YNUCalendar()
    events = parser.get_events()
    for e in events:
        #print(e['name'], e['term'])
        print(e['name'])
        print(e['term'])
