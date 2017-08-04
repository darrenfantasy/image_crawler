# /usr/bin/python
# encoding:utf-8

import requests
import json
from bs4 import BeautifulSoup
base_url = 'http://www.kuaidaili.com/free/'
kuai_proxy_list = []

def get_kuai_free_proxies(url):
	try:
		print "--------------------------get_kuai_freeproxy---------------------------"
		global kuai_proxy_list
		p = requests.get(url)
		html = p.text
		soup = BeautifulSoup(html,"html.parser")
		content = soup.find("div",id="list")
		tr_list = content.find_all("tr")
		for x in xrange(1,len(tr_list)):
			one_tr = tr_list[x]
			ip = one_tr.find_all("td")[0].text
			port = one_tr.find_all("td")[1].text
			kuai_proxy = ip+":"+port
			print kuai_proxy
			kuai_proxy_list.append(kuai_proxy)
		return kuai_proxy_list
	except Exception, e:
		print e
	finally:
		pass

def get_one_from_list():
	try:
		print "------------------requests timeout, change a new proxy------------------"
		global kuai_proxy_list
		del kuai_proxy_list[0]
		if len(kuai_proxy_list)<=5:
			get_kuai_free_proxies()
		return kuai_proxy_list[0]
	except Exception, e:
		print e
	finally:
		pass
get_kuai_free_proxies(base_url)