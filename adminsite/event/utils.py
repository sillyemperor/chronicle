# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from bs4 import BeautifulSoup


def html2lines(html_str):
    res = r'(?P<year>[前]?\d+[年]+)'
    rec = re.compile(res)
    res2 = r'(?P<year>[前]?\d+)[年]+(?P<text>\W+)'
    rec2 = re.compile(res2)
    soup = BeautifulSoup(html_str, 'html.parser')
    for tag in soup.find_all(lambda x: x.name == 'div' and rec.search(x.text)):
        m = rec2.search(tag.text)
        yield m.group('year'), m.group('text')



