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

api_uri='https://zh.wikipedia.org/w/api.php'
closeLog()

def nameyf(y):
	return './wiki_chronicle/%d%s.xml'%(abs(y),y<0 and 'BC' or 'Y')
	
def redir(y1,y2):
	titles=[]
	for y in range(y1,y2):
		if not os.path.exists(nameyf(y)):			
			continue
		with open(nameyf(y),'rt') as f:
			s=f.read()
			r=re.search(r'#REDIRECT\s+\[\[(.*?)\]\]',s)
			title=None
			if r:
				for g in r.groups():
					titles.append(g)
					break		
	titles=set(titles)
	
	for title in titles:
		y=None
		r=re.search(r'前(\d+?)年代',title)
		if r:
			for g in r.groups():
				y=int(g)
				break
		if not y:
			r=re.search(r'前(\d+?)世纪',title)
			if r:
				for g in r.groups():
					y=int(g)*100
					break
		if not y:
			continue
		newfn='./wiki_chronicle/r%dBC.xml'%abs(y)
		print newfn
		if os.path.exists(newfn):
			return
		try:
			if title and not os.path.exists(newfn):
				s,r=httpGet('http://zh.wikipedia.org/w/api.php',dict(
						format='xml'
						,action='query'
						,titles=title
						,prop='revisions'
						,rvprop='content'
						))
				with open(newfn,'w+') as f:
					f.write(s)				
		except Exception as ex:
			print s,ex

def getAndSave(y):
	if os.path.exists(nameyf(y)):			
		return
	try:
		s,r=httpGet('http://zh.wikipedia.org/w/api.php',dict(
				format='xml'
				,action='query'
				,titles='%s%d%s'%(y<0 and '前' or '',abs(y),y<0 and '年' or '年')
				,prop='revisions'
				,rvprop='content'
				))
		if not os.path.exists('./wiki_chronicle'):
			os.mkdir('wiki_chronicle')
		with open(nameyf(y),'w+') as f:
			f.write(s)
	except Exception as ex:
		print y
		#traceback.print_exc()

def getRecords(y):
	if not os.path.exists(nameyf(y)):
		return []
	ret=[]
	with open(nameyf(y),'rt') as f:
		xmldoc = minidom.parse(f)
		try:
			n= xmldoc.getElementsByTagName('api')[0].getElementsByTagName('query')[0].getElementsByTagName('pages')[0].getElementsByTagName('page')[0].getElementsByTagName('revisions')[0].getElementsByTagName('rev')[0]
			mu=n.childNodes[0].data.encode("utf8")
		
			type=None
			for i in  mu.split('\n'):
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
		except:
			pass
		return ret

def printYear(y):
	for l in getRecords(y):
		print l[0],l[1],'年',l[2],'月',l[3],'日',l[4] 


def loadFile(year,file):
	if not os.path.exists(file):
		return	
	with open(file,'rt') as f:
		s=f.read()
		r=re.search(r'#REDIRECT\s+\[\[(.*?)\]\]',s)
		rtitle=None
		if r:
			for g in r.groups():
				rtitle=g
				break
		if rtitle:
			y=None
			r=re.search(r'前(\d+?)年代',rtitle)
			if r:
				for g in r.groups():
					y=int(g)
					break
			if not y:
				r=re.search(r'前(\d+?)世纪',rtitle)
				if r:
					for g in r.groups():
						y=int(g)*100
						break
			if y:
				newfn='./wiki_chronicle/r%dBC.xml'%abs(y)								
				return loadFile(year,newfn)
		xmldoc = minidom.parseString(s)
		ret=[]
		try:
			n= xmldoc.getElementsByTagName('api')[0].getElementsByTagName('query')[0].getElementsByTagName('pages')[0].getElementsByTagName('page')[0].getElementsByTagName('revisions')[0].getElementsByTagName('rev')[0]
			mu=n.childNodes[0].data.encode("utf8")
		
			type=None
			for i in  mu.split('\n'):
				#print '>',i
				r=re.match(r'==\s+\[*?(.*?)\]*?\s+==',i)
				c=False
				if r:
					for g in r.groups():
						type=g
						c=True
						break				
				if c:
					continue
				#print type
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
					#print type,year,m,d,txt
					ret.append((type,year,m,d,txt))
		except:
			pass
		return ret
		
def mergeTimeline(y1,y2):
	date=[]
	for y in range(y1,y2):
		j=loadFile(y,nameyf(y))
		if j:
			for i in j:
				date.append(dict(
				startDate='%s,%s,%s'%(i[1],i[2] and i[2] or 0,i[3] and i[3] or 0)
				,endDate='%s,%s,%s'%(i[1],i[2] and i[2] or 0,i[3] and i[3] or 0)
				,headline=i[0]
				,text=i[-1].replace(']]','').replace('[[','')
				))
	with open('%d%s_%d%s.json'%(abs(y1),y1<0 and 'BC' or '',abs(y2),y2<0 and 'BC' or ''),'w+') as f:
		f.write(json.dumps(dict(
		timeline=dict(
		headline='World History'
		,type='default'
		,text='World History'
		,date=date
		)
		)))

def nameYear(y):
	return '%s%d%s'%(y<0 and '前' or '',abs(y),y<0 and '年' or '年')
def unnameYear(yname):
	r=re.match(r'(\d+?)年',yname)
	if r:
		for g in r.groups():
			return g
	return yname

def searchTimeFromWiki(y1,y2):
	try:
		s,r=httpGet('http://zh.wikipedia.org/w/api.php',dict(
				format='xml'
				,action='query'
				,titles='|'.join([nameYear(y) for y in range(y1,y2+1)])
				,prop='revisions'
				,rvprop='content'
				))
		ret=[]
		xmldoc = minidom.parseString(s)
		for n in xmldoc.getElementsByTagName('api')[0].getElementsByTagName('query'):
			for nn in n.getElementsByTagName('pages'):
				for nnn in nn.getElementsByTagName('page'):
					yname= nnn.getAttribute('title').encode('utf8')
					for nnnn in nnn.getElementsByTagName('revisions'):
						for nnnnn in nnnn.getElementsByTagName('rev'):
							for t in nnnnn.childNodes:
								ret+=parseRawText(unnameYear(yname),t.data.encode('utf8'))
		return ret
	except Exception as ex:
		print y1,y2,ex
		raise ex
def searchTimeFromLocal(y1,y2):
	ret=[]
	for y in range(y1,y2+0):
		ret+=getRecords(y)
	return ret

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
	
def timelimeJson(list,headline,text):
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
		,text=text
		,date=date
		)
		))

def cacheWikiToJson(y1,y2):
	ret=[]
	Y=None
	cacheId=1
	cache=[]
	for y in range(y1,y2+1):
		if not Y:
			Y=y
		ret+=getRecords(y)
		if len(ret)>100:
			t='公元%s--%s'%(nameYear(Y),nameYear(y))
			s=timelimeJson(ret,t,t)
			with open('./cache/%s.json'%cacheId,'w+') as f:
				f.write(s)
				cache.append(dict(id=cacheId,title=t,year1=Y,year2=y))
				cacheId+=1
			ret=[]
			Y=y
	with open('./cache/info.json','w+') as f:
		f.write(json.dumps(cache))

def cachedTimezones():
	with open('./cache/info.json','r') as f:
		return f.read()

def cachedTimezone(id):
	with open('./cache/%s.json'%id,'r') as f:
		return f.read()

if __name__=='__main__':
	pass
	#cacheWikiToJson(1,2013)

			
			



