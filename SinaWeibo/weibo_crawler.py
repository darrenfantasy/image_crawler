# !/usr/bin/python
# encoding:utf-8

from selenium import webdriver
import time
import requests
import json
from bs4 import BeautifulSoup
import os

cookie_save_file = "cookie.txt"
cookie_update_time_file = "cookie_timestamp.txt"
image_result_file = "image_result.md"
# username = 'your weibo accounts'##你的微博账号
# password = 'your weibo password'##你的微博密码

weibo_url = "http://weibo.com/"
requset_url = "http://weibo.com/p/aj/v6/mblog/mbloglist?"
example_weibo_id = "3278620272"##想爬取的微博号的ID
request_params = {"ajwvr":"6","domain":"100505","domain_op":"100505","feed_type":"0","is_all":"1","is_tag":"0","is_search":"0"}
profile_request_params = {"profile_ftype":"1","is_all":"1"}


headers = {
        'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
		'Cache-Control':'no-cache',
		'Connection':'keep-alive',
		'Content-Type':'application/x-www-form-urlencoded',
		'Host':'weibo.com',
		'Pragma':'no-cache',
		'Referer':'http://weibo.com/u/3278620272?profile_ftype=1&is_all=1',
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		'X-Requested-With':'XMLHttpRequest'
        }

def get_timestamp():##获取当前系统时间戳
    try:
        tamp = time.time()
        timestamp = str(int(tamp))+"000"
        print timestamp
        return timestamp
    except Exception, e:
        print e
    finally:
        pass

def login_weibo_get_cookies():##登录获取cookies
	time.sleep(2)
	driver.find_element_by_name("username").send_keys(username)##输入用户名
	driver.find_element_by_name("password").send_keys(password)##输入密码
	driver.find_element_by_xpath("//a[@node-type='submitBtn']").click()##点击登录按钮
	cookies = driver.get_cookies()##获取cookies
	print cookies
	cookie = ""
	##将返回的Cookies数组转成微博需要的cookie格式
	for x in xrange(len(cookies)):
		value = cookies[x]['name']+"="+cookies[x]['value']+";"
		cookie = cookie+value
	print cookie
	return cookie

def save_cookie(cookie):##把cookie存到本地
    try:
        if os.path.isfile(cookie_save_file)==False:
            os.system("touch "+cookie_save_file) 
        f= open(cookie_save_file,'w')
        f.write(cookie)
        f.close()
    except Exception, e:
        print e
    finally:
        pass

def get_cookie_from_txt():##从本地文件里读取cookie
	f = open(cookie_save_file)
	cookie = f.read()
	print cookie
	return cookie

def save_cookie_update_timestamp(timestamp):##把cookie存到本地
    try:
        if os.path.isfile(cookie_update_time_file)==False:
            os.system("touch "+cookie_update_time_file) 
        f= open(cookie_update_time_file,'w')
        f.write(timestamp)
        f.write('\n')
        f.close()
    except Exception, e:
        print e
    finally:
        pass

def get_cookie_update_time_from_txt():##获取上一次cookie更新时间
	try:
		if os.path.isfile(cookie_update_time_file)==False:
			os.system("touch "+cookie_update_time_file) 
		f = open(cookie_update_time_file)
		lines = f.readlines()
		cookie_update_time = lines[0]
		print cookie_update_time
		return cookie_update_time
	except Exception, e:
		print e
	finally:
		pass

def write_image_urls(image_list):
    try:
    	if os.path.isfile(image_result_file)==False:
    		os.system("touch "+image_result_file) 
    	f= open(image_result_file,'a+')
        for x in xrange(len(image_list)):
        	image = image_list[x]
        	show_image = "![]("+image+")"
        	f.write(show_image.encode("utf-8"))
        	f.write('\n')
        f.close()
    except Exception, e:
        print e
    finally:
        pass


def is_valid_cookie():##判断cookie是否有效
	if os.path.isfile(cookie_update_time_file)==False:
		return False
	else :
		f = open(cookie_update_time_file)
		lines = f.readlines()
		if len(lines) == 0:
				return False
		else :
			last_time_stamp = get_cookie_update_time_from_txt()
			if long(get_timestamp()) - long(last_time_stamp) > 6*60*60*1000:
				return False
			else :
				return True

def get_object_weibo_by_weibo_id_and_cookie(weibo_id,cookie,pagebar):##通过微博ID和cookie来调取接口
	try:
		headers["Cookie"] = cookie
		request_params["__rnd"] = get_timestamp()
		request_params["page"] = 1
		request_params["pre_page"] = 1
		request_params["pagebar"] = pagebar
		request_params["id"] = "100505"+weibo_id
		request_params["script_uri"] = "/u/"+weibo_id
		request_params["pl_name"] = "Pl_Official_MyProfileFeed__22"
		request_params["profile_ftype"] = 1
		response = requests.get(requset_url,headers=headers,params=request_params)
		html =  response.json()["data"]
		print html
		return html
	except Exception, e:
		print e
	finally:
		pass


def get_object_top_weibo_by_weibo_id_and_cookie(weibo_id,cookie):##每一页顶部微博
	try:
		profile_url = weibo_url+"u/"+weibo_id+"?"
		headers["Cookie"] = cookie
		response = requests.get(profile_url,headers=headers,params=profile_request_params)
		html = response.text
		# print html
		soup = BeautifulSoup(html,"html.parser")
		script_list = soup.find_all("script")
		script_size = len(script_list)
		# print script_list[script_size-1]
		html_start = str(script_list[script_size-1]).find("<div")
		html_end = str(script_list[script_size-1]).rfind("div>")
		print str(script_list[script_size-1])[html_start:html_end+4]
		return str(script_list[script_size-1])[html_start:html_end+4]
	except Exception, e:
		print e
	finally:
		pass



def get_img_urls_form_html(html):##从返回的Json中获取图片
	try:
		soup = BeautifulSoup(html,"html.parser")
		image_list = soup.find_all("img")
		image_url_list = []
		for x in xrange(len(image_list)):
			image_url = image_list[x].get("src").replace("\\","")
			print image_url
			image_url_list.append(image_url.replace("\"",""))
		return image_url_list
	except Exception, e:
		print e
	finally:
		pass


result = is_valid_cookie()
print result
if result == False:
	driver = webdriver.Chrome("/Users/fantasy/Downloads/chromedriver")##打开Chrome
	driver.maximize_window()##将浏览器最大化显示
	driver.get(weibo_url)##打开微博登录页面
	time.sleep(10)##因为加载页面需要时间，所以这里延时10s来确保页面已加载完毕
	cookie = login_weibo_get_cookies()
else :
	cookie = get_cookie_from_txt()
save_cookie(cookie)
save_cookie_update_timestamp(get_timestamp())
profile_html = get_object_top_weibo_by_weibo_id_and_cookie(example_weibo_id,cookie)
image_url_list = get_img_urls_form_html(profile_html)
write_image_urls(image_url_list)
for x in xrange(0,2):
	html = get_object_weibo_by_weibo_id_and_cookie(example_weibo_id,cookie,x)
	image_url_list = get_img_urls_form_html(html)
	write_image_urls(image_url_list)



