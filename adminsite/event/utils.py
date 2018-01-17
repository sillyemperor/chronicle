# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from bs4 import BeautifulSoup


def html2lines(html_str):
    res = r'[。]?(?P<year>[前]?\d+)[年]+(?P<text>\W+)[。]+'
    soup = BeautifulSoup(html_str, 'html.parser')
    s = soup.text
    for m in re.findall(res, s):
        yield m[0], m[1].replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")


def matchstr(s, matches, case_insensitive=False):
    """查询term，避免encoding错误"""
    m = set(matches)
    if case_insensitive:
        m2 = []
        for i in m:
            m2.append(i.upper())
            m2.append(i.lower())
        m = m2
    terms = [dict(
        i=0,
        j=0,
        t=i,
        f=False
    ) for i in m]
    i = 0
    n = len(s)
    r = []
    while i < n:
        c = s[i]
        for term in terms:
            if term['i'] >= len(term['t']):
                if not term['f']:
                    term['f'] = True
                    r.append(term['t'])
                continue
            if c == term['t'][term['i']]:
                term['j'] = i
                term['i'] += 1
            else:
                term['j'], term['i'] = 0, 0
        i += 1
    return r


