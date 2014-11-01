#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,os.path,imp,sys,urllib2,json,urllib
from xml.sax.saxutils import escape
import zlib
from http import *
import thread,threading
from xml.dom import minidom
from xml.dom.minidom import parse, parseString
import json
import re
import datetime
import traceback

closeLog()

def searchWiki(titles):
	s,r=httpGet('http://zh.wikipedia.org/w/api.php',dict(
				format='xml'
				,action='query'
				,titles=titles
				,prop='revisions'
				,rvprop='content'
				))
	return s

def nameYear(y):
	if y==1989: #Yeas,It`s necessary!
		return ''
	return '%s%d%s'%(y<0 and '前' or '',abs(y),y<0 and '年' or '年')
	
def unnameYear(yname):
	r=re.match(r'前(\d+?)年代',yname)
	if r:
		for g in r.groups():
			return '-%s'%g		
	r=re.match(r'(\d+?)年代',yname)
	if r:
		for g in r.groups():
			return g
	r=re.match(r'前(\d+?)年',yname)
	if r:
		for g in r.groups():		
			return '-%s'%g			
	r=re.match(r'(\d+?)年',yname)
	if r:
		for g in r.groups():
			return g
	return yname

def fnameYear(y):
	return '%d%s'%(abs(y),y<0 and 'BC' or 'AD')

def downloadWiki(y1,y2,dir):
	fname='%s/%s_%s.xml'%(dir,fnameYear(y1),fnameYear(y2))
	if os.path.exists(fname):
		return
	print fname
	titles= '|'.join([nameYear(y) for y in range(y1,y2)])
	s=searchWiki(titles)
	with open(fname,'w+') as f:
			f.write(s)	

def downloadFromWiki(y1,y2,dir):	
	if not os.path.exists(dir):
		os.mkdir(dir)
	step=50
	for y in range(y1,y2,step):#维基百科的query命令最多接受500个titles
		#print y,y+500>y2 and y2 or y+500
		threading.Thread(target=downloadWiki,args=[y,y+step>y2 and y2 or y+step,dir]).start()
	
def processRedirection(dir):
	if not os.path.exists(dir):
		return
	ry=[]
	for i in os.listdir(dir):
		with open(os.path.join(dir,i),'r') as f:
			r=re.search(r'#REDIRECT\s+\[\[(.*?)\]\]',f.read())
			if r:
				for g in r.groups():
					ry.append(g)
	s=searchWiki('|'.join(set(ry)))
	with open(os.path.join(dir,'redirections.xml'),'w+') as f:
			f.write(s)

def partWikiXml(f,destdir):
	xmldoc = minidom.parse(f)
	for n in xmldoc.getElementsByTagName('api')[0].getElementsByTagName('query'):
		for nn in n.getElementsByTagName('pages'):
			for nnn in nn.getElementsByTagName('page'):
				yname= nnn.getAttribute('title').encode('utf8')
				try:
					print yname
					y=int(unnameYear(yname))
					
					fyn='%d.txt'%(y+10000)
					print fyn
					for nnnn in nnn.getElementsByTagName('revisions'):
						for nnnnn in nnnn.getElementsByTagName('rev'):
							for t in nnnnn.childNodes:
								with open(os.path.join(destdir,fyn),'w+') as file:
									file.write(t.data.encode('utf8'))
								break
				except Exception as ex:
					print ex

def partXml(srcdir,destdir):
	if not os.path.exists(destdir):
		os.mkdir(destdir)
	for i in os.listdir(srcdir):
		partWikiXml(os.path.join(srcdir,i),destdir)
	
def parseRawText(y,s):
	ret=[]
	type=None
	for i in  s.split('\n'):
		#print '>',i
		r=re.match(r'==\s+\[*?(.*?)\]*?\s+==',i)
		c=False
		if r:
			for g in r.groups():
				type=g
				c=True
		if c:
			continue
		m=None
		d=None
		txt=None
		r=re.match('[*]+\s+\[*?(\d+?)月(\d+?)日\]*?(.*)',i)
		if r and len(r.groups())>2:
			ll=r.groups()
			m,d,txt=ll[0],ll[1],ll[2]
		if not txt:
			r=re.match('[*]+\s(.*)',i)
			if r and len(r.groups())>0:
					txt=r.groups()[0]
		if txt and type in ['大事記','大事记','出生','逝世','诺贝尔奖','奥斯卡金像奖'] :
			ret.append((type,y,m,d,txt))
	return ret

def parseWikiXml(f):
	ret=[]
	xmldoc = minidom.parse(f)
	for n in xmldoc.getElementsByTagName('api')[0].getElementsByTagName('query'):
		for nn in n.getElementsByTagName('pages'):
			for nnn in nn.getElementsByTagName('page'):
				yname= nnn.getAttribute('title').encode('utf8')
				for nnnn in nnn.getElementsByTagName('revisions'):
					for nnnnn in nnnn.getElementsByTagName('rev'):
						for t in nnnnn.childNodes:
							ret+=parseRawText(unnameYear(yname),t.data.encode('utf8'))
	return ret
	
def timelimeJson(list,headline,title):
	date=[]
	for i in list:
		text=i[-1].replace(']]','').replace('[[','')
		date.append(dict(
		startDate='%s,%s,%s'%(i[1],i[2] and i[2] or 0,i[3] and i[3] or 0)
		,endDate='%s,%s,%s'%(i[1],i[2] and i[2] or 0,i[3] and i[3] or 0)
		,headline='%s %s'%(i[0],text)
		,text=text
		))
	return json.dumps(dict(
		timeline=dict(
		headline=headline
		,type='default'
		,text=title
		,date=date
		)
		))

def buildTimelineJSJson(srcdir,destdir):
	if not os.path.exists(destdir):
		os.mkdir(destdir)
	years=[]
	for i in os.listdir(srcdir):
		y=int(i[:-4])
		years.append(y)
	list=[]
	Y=None
	cacheId=1
	cacheInfo=[]
	for i in sorted(years):
		with open(os.path.join(srcdir,'%d.txt'%i),'r') as fr:
			y=i-10000
			if not Y:
				Y=y
			for l in parseRawText(y,fr.read()):
				list.append(l)
				if len(list)>100:
					title='公元%s~%s'%(nameYear(Y),nameYear(y))
					with open(os.path.join(destdir,'%d.json'%cacheId),'w+') as fw:
						fw.write(timelimeJson(list,title,title))
						cacheInfo.append(dict(id=cacheId,title=title,year1=Y,year2=y))
						cacheId+=1
					list=[]
					Y=y
	with open(os.path.join(destdir,'info.json'),'w+') as f:
		f.write(json.dumps(cacheInfo))

if __name__=='__main__':
	wiki_download_dir='./wiki_files'
	#从维基下载数据！！！！本函数需要单独执行
	#downloadFromWiki(-1000,2013,wiki_download_dir)
	#有些年份被导引到特定年代，需要处理
	#processRedirection(wiki_download_dir)
	wiki_dir='./wiki_text'
	#分解成独立的文件，一年一个
	#partXml(wiki_download_dir,wiki_dir)
	json_cache_dir='./cache'
	#生成TimelineJS支持的json文件
	buildTimelineJSJson(wiki_dir,json_cache_dir)

			
			



