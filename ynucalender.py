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

    def _parse_term(self, term):
        year = self.get_year_num()
        terms = re.findall(u"(\d+)月(\d+)日", term)

        if len(terms) == 1:
            start = terms[0][0].zfill(2) + "-" + terms[0][1].zfill(2)
            end = start
        else:
            start = terms[0][0].zfill(2) + "-" + terms[0][1].zfill(2)
            end = terms[1][0].zfill(2) + "-" + terms[1][1].zfill(2)

        if start < '04-01':
            start = str(year + 1) + '-' + start
        else:
            start = str(year) + '-' + start

        if end < '04-01':
            end = str(year + 1) + '-' + end
        else:
            end = str(year) + '-' + end

        return {"start": start, "end": end}

    def _fetch_raw_html(self):
        connection = urllib2.urlopen(self._CALENDER_URL)
        raw_html = connection.read()
        connection.close()
        return raw_html

    def get_year_num(self):
        text = self._bs_inner.h2.get_text()
        nendo = re.search("\d+", text).group(0)
        return int(nendo) + 1988

    def get_info(self):
        info = []
        for tr in self._bs_inner.find_all("tr"):
            td = tr.find_all("td")
            term = self._parse_term(re.sub("[\n\r\t ]", "", td[1].get_text()))
            info.append({"summary": td[0].get_text(), "term": term})
        return info

    def get_raw_html(self):
        return self._raw_html

if __name__ == '__main__':
    pass
