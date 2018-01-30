# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import utils
import re
from bs4 import BeautifulSoup


class ImportFromURL(TestCase):
    def test_parse_q(self):
        years, word = utils.parse_q('-120~-100 凯撒')
        self.assertEquals(-120, years[0])
        self.assertEquals(-100, years[1])
        self.assertEquals('凯撒', word)

        years, word = utils.parse_q('-120~-100')
        self.assertEquals(-120, years[0])
        self.assertEquals(-100, years[1])
        self.assertIsNone(word)

        years, word = utils.parse_q('凯撒')
        self.assertIsNone(years)
        self.assertEquals('凯撒', word)

    def test_search(self):
        r = utils.matchstr('<med a="chartset:GB2312">',('gb2312', 'UTF-8', 'utf8'), True)
        self.assertEquals('GB2312', r[0])

    def test_re_year(self):
        res = r'(?P<year>[前]?\d+)[年]+'
        m = re.search(res, u'354.约公元前1600年—约公元前1046年')
        self.assertEquals('前1600', m.group('year'))
        m = re.search(res, u'304年')
        self.assertEquals('304', m.group('year'))

        res = r'(?P<year>[前]?\d+)[年]+(?P<text>\W+)'
        m = re.search(res, '309年，前赵帝刘渊迁都平阳，领有山西中部地区。 八月，前赵刘聪第一次进攻洛阳，战败。十月，前赵刘聪第二次进攻洛阳，战败 。')
        self.assertEquals('309', m.group('year'))
        self.assertEquals('，前赵帝刘渊迁都平阳，领有山西中部地区。 八月，前赵刘聪第一次进攻洛阳，战败。十月，前赵刘聪第二次进攻洛阳，战败 。', m.group('text'))

        res = r'[。]?(?P<year>[前]?\d+)[年]+(?P<text>[^。]+)[。]+'
        matches = re.findall(res, '后周世宗在稳定国内后即意图统一天下，他以“十年开拓天下，十年养百姓，十年致太平”为目标。955年率军击溃后蜀，占秦州汉中一带。956年率兵击溃南唐，获得江北之地，迫南唐称臣。959年后周世宗率军北伐辽朝以收复燕云十六州，周军陆续攻陷瀛洲、莫州等地。当他准备收复幽州时，却突然生病，被迫班师。[10]  不久去世，其幼子柴宗训即位，即后周恭帝。960年禁军领袖赵匡胤以镇定二州遭北汉、辽朝入侵为由率军北御，而后在开封的陈桥驿发生陈桥兵变，受禁军拥护为帝。赵匡胤回师开封，废黜后周恭帝，后周灭亡，五代结束。他建立宋朝，即宋太祖。')
        for m1, m2 in zip(matches, [
            ['955', '率军击溃后蜀，占秦州汉中一带'],
            ['956', '率兵击溃南唐，获得江北之地，迫南唐称臣'],
            ['959', '后周世宗率军北伐辽朝以收复燕云十六州，周军陆续攻陷瀛洲、莫州等地'],
            ['960', '禁军领袖赵匡胤以镇定二州遭北汉、辽朝入侵为由率军北御，而后在开封的陈桥驿发生陈桥兵变，受禁军拥护为帝'],
        ]):
            # print m1[1] travis 每次执行到这里都会报错 UnicodeEncodeError: 'ascii' codec can't encode 
            self.assertEquals(m2[0], m1[0])
            self.assertEquals(m2[1], m1[1])


    def test_parse_lines(self):
        html_str = '''
<html><head><title>The Dormouse's story</title></head>
<body>        
<div class="para" label-module="para">304年，<a target=_blank href="/item/%E7%9B%8A%E5%B7%9E/65621" data-lemmaid="65621">益州</a>氐族难民领袖李雄，于成都称<a target=_blank href="/item/%E6%88%90%E9%83%BD%E7%8E%8B">成都王</a>，建立成帝国。匈奴左贤王<a target=_blank href="/item/%E5%88%98%E6%B8%8A/9234" data-lemmaid="9234">刘渊</a>于山西离石称<a target=_blank href="/item/%E5%A4%A7%E5%8D%95%E4%BA%8E">大单于</a>，建立前赵。</div>
<div class="para" label-module="para">306年，成<a target=_blank href="/item/%E6%9D%8E%E9%9B%84/4031295" data-lemmaid="4031295">李雄</a>自称皇帝，国号“成”。</div>
<div class="para" label-module="para">307年，晋东海王<a target=_blank href="/item/%E5%8F%B8%E9%A9%AC%E8%B6%8A">司马越</a>毒死惠帝<a target=_blank href="/item/%E5%8F%B8%E9%A9%AC%E8%A1%B7">司马衷</a>，立怀帝<a target=_blank href="/item/%E5%8F%B8%E9%A9%AC%E7%82%BD">司马炽</a>，八王之乱结束。鲜卑慕容嵬自称大单于，<a target=_blank href="/item/%E7%9F%B3%E5%8B%92">石勒</a>投效前赵。<div class="lemma-picture text-pic layout-right" style="width:220px; float: right;">
<a class="image-link" nslog-type="9317" 
			href="/pic/%E4%BA%94%E8%83%A1%E4%B9%B1%E5%8D%8E/741526/0/b17eca8065380cd7adc7b371a844ad3458828154?fr=lemma&ct=single" target="_blank"
		title="" style="width:220px;height:146px;">
<img  class="lazy-img" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAMAAAAoyzS7AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAAZQTFRF9fX1AAAA0VQI3QAAAAxJREFUeNpiYAAIMAAAAgABT21Z4QAAAABJRU5ErkJggg==" data-src="https://gss0.bdstatic.com/-4o3dSag_xI4khGkpoWK1HF6hhy/baike/s%3D220/sign=7ff2498e464a20a4351e3bc5a0509847/b17eca8065380cd7adc7b371a844ad3458828154.jpg"  alt="" style="width:220px;height:146px;"/>
</a>
</div></div>
<div class="para" label-module="para">308年，前赵刘渊正式称帝。</div>
<div class="para" label-module="para">309年，前赵帝刘渊迁都<a target=_blank href="/item/%E5%B9%B3%E9%98%B3/3819522" data-lemmaid="3819522">平阳</a>，领有山西中部地区。 八月，前赵刘聪第一次进攻洛阳，战败。十月，前赵刘聪第二次进攻洛阳，战败 。</div>
<div class="para" label-module="para">310年，前赵帝刘渊死，子<a target=_blank href="/item/%E5%88%98%E5%92%8C/5966" data-lemmaid="5966">刘和</a>继位，<a target=_blank href="/item/%E5%88%98%E8%81%AA/31641" data-lemmaid="31641">刘聪</a>杀刘和，篡位。</div>
</body></html>        
        '''
        for i in utils.html2lines(html_str):
            print i

    # def test_parse_lines_whole(self):
    #     with open('event/test-data/wuhuluanhua.htm') as fp:
    #         for i in utils.html2lines(fp.read()):
    #             print i

    # def test_parse_lines_url(self):
    #     import requests
    #     import codecs
    #     response = requests.get('https://baike.baidu.com/item/%E4%BA%94%E8%83%A1%E4%B9%B1%E5%8D%8E', headers={
    #         # https://stackoverflow.com/questions/23651947/python-requests-requests-exceptions-toomanyredirects-exceeded-30-redirects
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
    #     })
    #     response.encoding  = 'utf-8'
    #     html_str = response.text
    #     print type(html_str)
    #     with codecs.open('event/test-data/wuhuluanhua2.htm', 'w', encoding='utf8') as fp:
    #         fp.write(html_str)
    #     for i in utils.html2lines(html_str):
    #         print i





