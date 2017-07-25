# /usr/bin/python
# encoding:utf-8

import requests
import json
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

base_url = 'http://www.ip181.com/'
proxy_list = []


def get_181_free_proxies():
	try:
		print "--------------------------get_181_freeproxy---------------------------"
		global proxy_list
		p = requests.get(base_url)
		requests.encoding = "gb2312"
		html = p.text
		soup = BeautifulSoup(html,"html.parser")
		content = soup.find("tbody")
		tr_list = content.find_all("tr")
		for x in xrange(1,len(tr_list)):
			one_tr = tr_list[x]
			ip = one_tr.find_all("td")[0].text
			port = one_tr.find_all("td")[1].text
			kuai_proxy = ip+":"+port
			print kuai_proxy
			proxy_list.append(kuai_proxy)
		return proxy_list
	except Exception, e:
		print e
	finally:
		pass

def get_one_from_list():
	try:
		print "------------------requests timeout, change a new proxy------------------"
		global proxy_list
		del proxy_list[0]
		if len(proxy_list)<=5:
			get_181_free_proxies()
		return proxy_list[0]
	except Exception, e:
		print e
	finally:
		pass