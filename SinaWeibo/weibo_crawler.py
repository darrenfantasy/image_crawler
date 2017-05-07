# !/usr/bin/python
# encoding:utf-8
'''
爬取微博的流程：因为微博调用接口的时候需要cookie,所以我们要用webdriver来登录微博获取cookie,微博的cookie有效期应该蛮长的，我设置过期时间6hours,未过期则去本地读取，否则重新登录获取cookie
获取cookie后则分析微博网页端的请求，找到相应接口和参数，然后去请求我们要的数据。
这个例子是去获取微博里的图片，例子爬取的微博是我伦的官方账号：MRJ台灣官方
运行代码脚本需要加5个参数 分别为 1.微博账号 2.微博密码 3.要爬取的账号的个性域名（无个性域名则输入 u/+微博id）4.要爬取的账号的ID 5.爬取页数
如：python weibo_crawler.py username password mrj168 1837498771 5
'''
from selenium import webdriver
import time
import requests
import json
from bs4 import BeautifulSoup
import os
import sys

request_params = {"ajwvr":"6","domain":"100505","domain_op":"100505","feed_type":"0","is_all":"1","is_tag":"0","is_search":"0"}
profile_request_params = {"profile_ftype":"1","is_all":"1"}

weibo_url = "http://weibo.com/"
requset_url = "http://weibo.com/p/aj/v6/mblog/mbloglist?"


cookie_save_file = "cookie.txt"#存cookie的文件名
cookie_update_time_file = "cookie_timestamp.txt"#存cookie时间戳的文件名
image_result_file = "image_result.md"#存图片结果的文件名


# username = 'your weibo accounts'##你的微博账号
# password = 'your weibo password'##你的微博密码

person_site_name = "mrj168"#想爬取的微博号的个性域名 无个性域名则换成: u/+"微博id" 如 u/12345678
weibo_id = "1837498771"#微博id可以在网页端打开微博，显示网页源代码，找到关键词$CONFIG['oid']='1837498771'; 
page_size = 5#你要爬取的微博的页数






headers = {#User-Agent需要根据每个人的电脑来修改
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

def get_timestamp():#获取当前系统时间戳
    try:
        tamp = time.time()
        timestamp = str(int(tamp))+"000"
        print timestamp
        return timestamp
    except Exception, e:
        print e
    finally:
        pass

def login_weibo_get_cookies():#登录获取cookies
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

def save_cookie(cookie):#把cookie存到本地
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

def get_cookie_from_txt():#从本地文件里读取cookie
	f = open(cookie_save_file)
	cookie = f.read()
	print cookie
	return cookie

def save_cookie_update_timestamp(timestamp):#把cookie存到本地
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

def get_cookie_update_time_from_txt():#获取上一次cookie更新时间
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


def is_valid_cookie():#判断cookie是否有效
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

def get_object_weibo_by_weibo_id_and_cookie(weibo_id,person_site_name,cookie,pagebar,page):#通过微博ID和cookie来调取接口
	try:
		headers["Cookie"] = cookie
		headers['Referer'] = weibo_url+person_site_name+"?profile_ftype=1&is_all=1"
		request_params["__rnd"] = get_timestamp()
		request_params["page"] = page
		request_params["pre_page"] = page
		request_params["pagebar"] = pagebar
		request_params["id"] = "100505"+weibo_id
		request_params["script_uri"] = "/"+person_site_name
		request_params["pl_name"] = "Pl_Official_MyProfileFeed__22"
		request_params["profile_ftype"] = 1
		response = requests.get(requset_url,headers=headers,params=request_params)
		print response.url
		html =  response.json()["data"]
		return html
	except Exception, e:
		print e
	finally:
		pass


def get_object_top_weibo_by_person_site_name_and_cookie(person_site_name,cookie,page):#每一页顶部微博
	try:
		profile_url = weibo_url+person_site_name+"?"
		headers["Cookie"] = cookie
		profile_request_params["page"] = page
		response = requests.get(profile_url,headers=headers,params=profile_request_params)
		print response.url
		html = response.text
		soup = BeautifulSoup(html,"html.parser")
		script_list = soup.find_all("script")
		script_size = len(script_list)
		print "script_size:"+str(script_size)
		tag = 0
		for x in xrange(script_size):
			if "WB_feed WB_feed_v3 WB_feed_v4" in str(script_list[x]):
				tag = x
		print "tag:"+str(tag)
		# print script_list[script_size-1]
		html_start = str(script_list[tag]).find("<div")
		html_end = str(script_list[tag]).rfind("div>")
		# print str(script_list[tag])[html_start:html_end+4]
		return str(str(script_list[tag])[html_start:html_end+4])
	except Exception, e:
		print e
	finally:
		pass



def get_img_urls_form_html(html):#从返回的html格式的字符串中获取图片
	try:
		image_url_list = []
		result_html = html.replace("\\","")
		soup = BeautifulSoup(result_html,"html.parser")
		div_list = soup.find_all("div",'media_box')
		print "div_list:"+str(len(div_list))
		for x in xrange(len(div_list)):
			image_list = div_list[x].find_all("img")
			for y in xrange(len(image_list)):
				image_url = image_list[y].get("src").replace("\\","")
				print image_url
				image_url_list.append(image_url.replace("\"",""))			
		return image_url_list
	except Exception, e:
		print e
	finally:
		pass

if(len(sys.argv)==6):
	username = sys.argv[1]
	password = sys.argv[2]
	person_site_name = sys.argv[3]
	weibo_id = sys.argv[4]
	page_size = int(sys.argv[5])
	print "微博账号："+username
	print "微博密码："+password
	print "要爬取的账号的个性域名（无个性域名则输入 u/+微博id ）："+person_site_name
	print "要爬取的账号的ID："+weibo_id
	print "爬取页数："+str(page_size)
else:
	print "未按照指定参数输入，请按顺序输入5个指定参数 1.微博账号 2.微博密码 3.要爬取的账号的个性域名（无个性域名则输入 u/+微博id）4.要爬取的账号的ID 5.爬取页数"
	sys.exit(0)

result = is_valid_cookie()
print result
if result == False:
	driver = webdriver.Chrome("/Users/darrenfantasy/Documents/study/python/image_crawler/SinaWeibo/chromedriver")#打开Chrome
	driver.maximize_window()#将浏览器最大化显示
	driver.get(weibo_url)#打开微博登录页面
	time.sleep(10)#因为加载页面需要时间，所以这里延时10s来确保页面已加载完毕
	cookie = login_weibo_get_cookies()
	save_cookie(cookie)
	save_cookie_update_timestamp(get_timestamp())
else :
	cookie = get_cookie_from_txt()
for x in xrange(1,page_size+1):
	profile_html = get_object_top_weibo_by_person_site_name_and_cookie(person_site_name,cookie,x)
	image_url_list = get_img_urls_form_html(profile_html)
	write_image_urls(image_url_list)
	for y in xrange(0,2):#有两次下滑加载更多的操作
		print "pagebar:"+str(y)
		html = get_object_weibo_by_weibo_id_and_cookie(weibo_id,person_site_name,cookie,y,x)
		image_url_list = get_img_urls_form_html(html)
		write_image_urls(image_url_list)




