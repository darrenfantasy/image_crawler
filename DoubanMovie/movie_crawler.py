#encoding:utf-8

import requests
import json
import os,sys,time
from lxml import etree
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
import re
reload(sys)
sys.setdefaultencoding("utf-8")

LANGUAGES_RE = re.compile(ur"语言:</span> (.+?)<br>")
COUNTRIES_RE = re.compile(ur"制片国家/地区:</span> (.+?)<br>")
ALTERNATE_NAME_RE = re.compile(ur"又名:</span> (.+?)<br>")
RELEASE_TIME_RE = re.compile(ur"上映日期:</span> (.+?)<br>")
NUM_RE = re.compile(r"(\d+)")

data_save_file = "douban_donghua_results.txt"
headers = {
	'Accept':'*/*',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
	'Connection':'keep-alive',
	'Host':'movie.douban.com',
	'Referer':'https://movie.douban.com/explore',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}

def get_item_list(d_url,d_type,d_tag,d_sort,d_page_limit,d_page_start):
	params = {}
	params["type"] = d_type
	params["tag"] = d_tag
	if d_sort != "":
		params["sort"] = d_sort
	params["page_limit"] = d_page_limit
	params["page_start"] = d_page_start
	response = requests.get(d_url,headers = headers,params = params,timeout =10)
	json_obj = response.json()
	json_array = json_obj["subjects"]
	return json_array

def get_item_list_from_newsearch(d_url,d_sort,d_range,d_tag,d_page_start):
	params = {}
	params["sort"] = d_sort
	params["tags"] = d_tag
	params["range"] = d_range
	params["start"] = d_page_start
	response = requests.get(d_url,headers = headers,params = params,timeout =10)
	json_obj = response.json()
	json_array = json_obj["data"]
	return json_array
def get_item_detail(item_detail_url):
	result_obj = {}
	result_obj["subject_id"] = int(item_detail_url.split("/")[-2])
	celebrities_url = "https://movie.douban.com/subject/"+str(result_obj["subject_id"])+"/celebrities"
	(directors_cn_names,directors_en_names,actors_cn_names,actors_en_names)=get_directors_and_actors(celebrities_url)
	result_obj["directors_cn_names"] = directors_cn_names
	result_obj["directors_en_names"] = directors_en_names
	result_obj["actors_cn_names"] = actors_cn_names
	result_obj["actors_en_names"] = actors_en_names
	response = requests.get(item_detail_url,headers = headers,timeout = 10)
	selector = etree.HTML(response.text)
	s_response = HtmlResponse(url=item_detail_url,body = response.text,encoding='utf-8')

	name = s_response.selector.xpath("//title/text()").extract()
	if name: result_obj["movie_name"] = name[0].replace(u" (豆瓣)", "").strip()

	genres = s_response.selector.xpath("//span[@property='v:genre']/text()").extract()
	if genres: result_obj["genres"] = genres

	S = "".join(s_response.selector.xpath("//div[@id='info']").extract())

	M = COUNTRIES_RE.search(S)
	if M is not None:
		result_obj["countries"] = [country.strip() for country in M.group(1).split("/")]
	
	L = LANGUAGES_RE.search(S)
	if L is not None:
		result_obj["languages"] = [ lang.strip() for lang in L.group(1).split("/") ]

	A = ALTERNATE_NAME_RE.search(S)
	if A is not None:
		result_obj["alternate_name"] =[ alternate.strip() for alternate in A.group(1).split("/")]

	T = []
	tags = s_response.selector.xpath("//div[@class='tags-body']/a")
	for tag in tags:
		t = tag.xpath("text()").extract()
		if t: T.append(t[0])
	if T: result_obj["tags"] = T

	average = s_response.selector.xpath("//strong[@property='v:average']/text()").extract()
	if average and average[0] != "": result_obj["average"] = float( average[0] ) + 0.0

	json_value = json.dumps(result_obj,ensure_ascii = False)
	print(json_value)
	return json_value

def get_directors_and_actors(celebrities_url):
	try:
		p = requests.get(celebrities_url,headers = headers)
		html = p.text
		soup = BeautifulSoup(html,"html.parser")
		div_list = soup.find_all("div","list-wrapper")
		directors_html = div_list[0]
		directors = directors_html.find_all("a")
		directors_cn_names = []
		directors_en_names = []
		actors_cn_names = []
		actors_en_names = []
		for x in xrange(len(directors)):
			if directors[x].get("target") != "_blank":
				director = directors[x].text
				first_tag = director.find(" ")
				directors_cn_name = director[:first_tag].strip()
				directors_en_name = director[first_tag+1:].strip()
				if directors_cn_name != "":
					directors_cn_names.append(directors_cn_name)
				if directors_en_name != "":
					directors_en_names.append(directors_en_name)
				print directors_cn_name
				print directors_en_name

		actors_html = div_list[1]
		actors = actors_html.find_all("a")
		for x in xrange(len(actors)):
			if actors[x].get("target") != "_blank":
				actor = actors[x].text
				first_tag = actor.find(" ")
				actors_cn_name = actor[:first_tag].strip()
				actors_en_name = actor[first_tag+1:].strip()
				if actors_cn_name != "":
					actors_cn_names.append(actors_cn_name)
					print "cn_name: "+actors_cn_name
				if actors_en_name != "":
					actors_en_names.append(actors_en_name)
					print "en_name: "+actors_en_name
	except Exception, e:
		print e
		directors_cn_names = []
		directors_en_names = []
		actors_cn_names = []
		actors_en_names = []
	finally:
		return (directors_cn_names,directors_en_names,actors_cn_names,actors_en_names)



def write_json_obj(json_value):
    os.system("touch "+data_save_file)
    f= open(data_save_file,'a+')
    f.write(str(json_value)+",")
    f.close()

search_url = "https://movie.douban.com/j/search_subjects?"
tag_search_url = "https://movie.douban.com/j/new_search_subjects?"

#豆瓣电影-选电影下的爬虫，如下例子是经典里的前50页
for x in xrange(0,50):
	print x
	page_start = 20*x
	print page_start
	time.sleep(1)
	json_array = get_item_list(search_url,"movie","经典","time",20,page_start)
	for x in xrange(len(json_array)):
		time.sleep(1)
		json_value = get_item_detail(json_array[x]["url"])
		write_json_obj(json_value)

#豆瓣电影-分类下的爬虫，如下例子是动画里的前50页
for x in xrange(0,50):
	print x
	page_start = 20*x
	print page_start
	time.sleep(1)
	json_array = get_item_list_from_newsearch(tag_search_url,"T","0,10","动画",page_start)
	for x in xrange(len(json_array)):
		time.sleep(1)
		json_value = get_item_detail(json_array[x]["url"])
		write_json_obj(json_value)


