# !/usr/bin/python
# encoding:utf-8

from selenium import webdriver
import time

username = 'your weibo accounts'##你的微博账号
password = 'your weibo password'##你的微博密码
weibo_url = "http://weibo.com/"


def login_weibo_get_cookies():##登录获取cookies
	time.sleep(2)
	driver.find_element_by_name("username").send_keys(username)##输入用户名
	driver.find_element_by_name("password").send_keys(password)##输入密码
	driver.find_element_by_xpath("//a[@node-type='submitBtn']").click()##点击登录按钮
	cookies = driver.get_cookies()##获取cookies
	print cookies
	return cookies



driver = webdriver.Chrome("/Users/fantasy/Downloads/chromedriver")##打开Chrome
driver.maximize_window()##将浏览器最大化显示
driver.get(weibo_url)##打开微博登录页面
time.sleep(10)##因为加载页面需要时间，所以这里延时10s来确保页面已加载完毕
login_weibo_get_cookies()


