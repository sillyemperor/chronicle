# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from bs4 import BeautifulSoup


def trim(s):
    return s.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")


def parse_q(q):
    years = None
    word = q
    m = re.match(r'^(?P<years>[-]?\d+[~][-]?\d+)', q)#
    if m:
        groups = m.groupdict()
        if 'years' in groups:
            years = map(int, groups['years'].split('~'))
            m = re.search(r'[ ]{1}(?P<word>.+)', q)
            if m:
                groups = m.groupdict()
                if 'word' in groups:
                    word = trim(groups['word'])
            else:
                word = None
    return years, word


def html2lines(html_str):
    # res = r'[。]?(?P<year>[前]?\d+)[年]+(?P<text>[^。]+)[。]+'
    soup = BeautifulSoup(html_str, 'html.parser')
    s = soup.text
    return text2sentences(s)
    # for m in re.findall(res, s):
    #     ym = re.match(r'[前]?(?P<year>\d+)', m[0])
    #     if ym:
    #         ys = ym.group('year')
    #         yield trim(m[1]), '%s%s'%(('前' in m[0] and '-' or ''), ys)


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


def text2sentences(text):
    ret = []
    for l in text.split('。'):
        m = re.search(r'(?P<year1>[前]?\d+)年([~](?P<year2>[前]?\d+)年)?', l)
        if m:
            y1 = m.group('year1')
            ym = re.search(r'[前]?(?P<year>\d+)', y1)
            ys = ym.group('year')
            year1 = '%s%s'%(('前' in y1 and '-' or ''), ys)
            year2 = ''
            y1 = m.group('year2')
            if y1:
                ym = re.search(r'[前]?(?P<year>\d+)', y1)
                ys = ym.group('year')
                year2 = '%s%s' % (('前' in y1 and '-' or ''), ys)
            ret.append((trim(l), year1, year2))
        else:
            m = re.search(r'（(?P<year1>[前]?\d+)）', l)
            if m:
                y1 = m.group('year1')
                ym = re.search(r'[前]?(?P<year>\d+)', y1)
                ys = ym.group('year')
                year1 = '%s%s' % (('前' in y1 and '-' or ''), ys)
                year2 = ''
                ret.append((trim(l), year1, year2))

    return ret

