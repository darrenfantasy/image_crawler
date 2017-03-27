# !/usr/bin/python
# encoding:utf-8

from selenium import webdriver
import time

# username = 'your weibo accounts'##你的微博账号
# password = 'your weibo password'##你的微博密码
weibo_url = "http://weibo.com/"



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



driver = webdriver.Chrome("/Users/fantasy/Downloads/chromedriver")##打开Chrome
driver.maximize_window()##将浏览器最大化显示
driver.get(weibo_url)##打开微博登录页面
time.sleep(10)##因为加载页面需要时间，所以这里延时10s来确保页面已加载完毕
login_weibo_get_cookies()


