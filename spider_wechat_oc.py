#!/usr/bin/python
#coding:utf-8
import urllib2  
import requests
import json
from bs4 import BeautifulSoup

def cut_url(a):
    i = -1
    while a[i] != '.':
        i -= 1
    return a[i:]

def get_html(html):
    name_num = 0
    soup = BeautifulSoup(html, "html.parser")
    for detail in soup.find_all('img'):
        image = detail.get('data-src')
        if image is None:
            pass
        else:
            name_num += 1
            # pic = requests.get(image, verify=False)
            # pic_name = str(name_num) + str(cut_url(image))
            print u'the%dphoto, img url：%s\n' % (name_num,image)
            # with open(address + '\\' + pic_name, 'wb') as fp:
            #     fp.write(pic.content)
    print u"\nfinish   all%dphoto ╰(￣▽￣)╭ \n " % name_num


def getHistoryUrlByWechatId(url):
	soup = BeautifulSoup(url, "html.parser")
	a = soup.find('a',uigs="main_toweixin_account_image_0")
	resUrl = a.get('href')
	return resUrl

def getOnePageContentUrl(html):
    name_num = 0
    start = 0
    end = 0
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find_all('script')[8]
    # print u'content.string:%s' % (content)
    size =len(content.string)
    # print u'size:%d' %size
    start = content.string.find("msgList")
    end = content.string.rfind("}")
    # print u'start:%d' %start
    result = content.string[start+10:end+1]
    # print u'%s' %result
    s = json.loads(result)
    urlList = []
    for x in xrange(len(s["list"])):
        addUrl = "http://mp.weixin.qq.com"+s["list"][x]["app_msg_ext_info"]["content_url"]
        newUrl = addUrl.replace('&amp;','&')
        urlList.append(newUrl)
    return urlList

wechatIdList = ['','','']//“你要爬的公众号id列表”
for x in xrange(len(wechatIdList)):
    print wechatIdList[x]
    baseUrl = 'http://weixin.sogou.com/weixin?type=1&query='+wechatIdList[x]+'&ie=utf8&_sug_=y&_sug_type_=1'
    response = urllib2.urlopen(baseUrl) 
    content = response.read()
    historyUrl = getHistoryUrlByWechatId(content)
    print u'historyUrl:%s' % (historyUrl)
    response2 = urllib2.urlopen(historyUrl) 
    urls =getOnePageContentUrl(response2)
    for x in xrange(len(urls)):
        print urls[x]
        response = urllib2.urlopen(urls[x])  
        content = response.read()  
        get_html(content)


