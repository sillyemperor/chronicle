#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,os.path,imp,sys,urllib2,json,urllib
from xml.sax.saxutils import escape
import thread,threading

log=True

def openLog():
	global log
	log=True
def closeLog():
	global log
	log=False

def httpPost(url,data=None,headers=None):
	global log
	import time
	if log:print url
	t=time.time()
	req = urllib2.Request(url=url,
		data=(data and urllib.urlencode(data) or None))
	if headers:
		for k,v in headers.iteritems():
			req.add_header(k, v)
	resp=urllib2.urlopen(req)
	s=resp.read()
	if log:print s,time.time()-t
	if log:print
	return s,resp
	
def httpGet(url,data=None,headers=None):
	global log
	import time
	url='%s?%s'%(url,(data and urllib.urlencode(data) or ''))
	if log:print url
	t=time.time()
	req = urllib2.Request(url=url)
	if headers:
		for k,v in headers.iteritems():
			req.add_header(k, v)
	resp=urllib2.urlopen(req)
	s=resp.read()
	if log:print s,time.time()-t
	if log:print
	return s,resp
