#! /usr/bin/python
#encoding:utf-8
'''
花瓣网爬虫，以花瓣下的旅行模块为例 http://huaban.com/favorite/travel_places/
main_page中的max参数对应的是起始的ID,可以点击某个图片进入详情即可看到
如示例代码中的max参数的值，就是点击这个图片进入详情页后的ID http://huaban.com/pins/1082254826/
一页爬取20个，爬取完一页后以接口返回的Json中的最后一个的 pin_id 为下一次请求的max的参数
huaban_travel_places_result.txt 为运行的结果
'''


import json
import os
import requests

main_page = "http://huaban.com/favorite/travel_places/?j0x9q48g&max=1082254826&limit=20&wfl=1"
save_result_path = "huaban_travel_places_result.txt"

headers = {
			'Accept':'application/json',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
			'Cache-Control':'no-cache',
			'Connection':'keep-alive',
			'Cookie':'BDTUJIAID=f6b17872d06259f8a38509c1baf402e9; UM_distinctid=15adb12a1f22b5-0b1ea1d4ebe05e-1d396850-1fa400-15adb12a1f3672; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAAFjElEQVRYR7WWeWxUVRTGf2fa6UIrNUIRi0VBqMiq4mtBAp2JBhODAQE1aoJhp%2BDGvgkIQgAx0PlDQIIlxhiwEjBCMEikU9EiMwVFG0ooFGQxgWKRWKTQzhxz%2B96UKXul3GQyL%2B%2Bdd%2B%2F5zvd95zxBVXHWzMWLaXv8OONXrkRF6u6qSB%2FgG%2BABgZpI7O3%2BK8wEkgVm3%2B4714vLrcytz%2FN6zyUayLjVq0k%2FcYLZixbVx6pIV2AHkC4QamwyCuOAlgILG%2FtudHyjgWQcOsSk5cuJra0lFBND2OV6AvgS6Ay8BKQAa4BXgI7ACoEqhRbA20Br4C%2FgI4FKhZHAamAV8BwwRqCwjm0YgP27BPwkkK%2BQ6hQuD3gXWAss8VXm3rSIDRgZkZfHxxMmsGTGDOIvXaI6IYH58%2BZ95oDoDTQHfgMetvNgH9Af%2BAf4FXgGOAscAHoJnHEYyRCYpPA48AvwCPA00A6bKVOgTIEpCu8B8wAL%2BAMoM%2Bf7KnNP34zRBkCMN1qePcuCuXOjpZWBXcF0oBmwxUk47HjHVLwtMFBgjoIx13rDjgNkPNDGeMR5FgSmA3OAFwXOqc32GwLT1T5jW9QZm4CxjQIyfN06Ohw%2BfLVHugCbgceAJKAEaA9EgLzmVHi%2BwEAn2d%2BBvk6SBojxyIIoIJOABUCOQKlCtpGYwNTrADGNZpivMrfythhpX17OqpwcatxuDKCK1NQ6n9S43e8ASwEvYKq5H8gH3NgyMNJYBpjkTSUNQJP8t46PRgBvAi8APYHRwLOONwxz7wOjgA7AEOBf4Csgy7kuAkb4KnPNfjdc9dLqWlLC5bg4YkIhLsXHU96%2BPQnV1VxMTOzhbGgoN2y0AvoBPwP3OZ44BcQDplUfA847ctqvtiQTnUQvGpmKDdaYrJPTHHYD3YFyIA0wcWY%2FE1cLxPoqc43vbg3kxhHOQLmT3tkE7zaq%2FV73PLkWiBbuaYdKPioXENwopeK1Rqk%2FsAXEsJSAsFKyrU8je%2BqPxW2p1fWopoAsFK%2B14erz1B%2FYhJKBS3ZItjXx6jkiCkOPdGNvq1OUN29omQZd63aB1MmiIDgUqZsv28VjPW%2FfK4hFkk4hki%2FZ1lv1IMx9kg%2BDbiQ2Zj2h0E5EPJJtmVZct9QfNP5KQauykeRyVNaI96n6Ifr5n2t0cHkXmtXGse2hg5SlmFF1Zf1vIPbhAaPtLmhSmni7VOmuvT0JhXeQGO4oWVn1J6k%2FYMzvI1Fbm%2FvqDxSB%2FF1fgOLiFKq0AnUNFm%2FPreovng86SjxWm0iq3x%2FeoK6wkHUmHX9aOYfuNeOqqYDYrJgOM0081jL1B74AaSkey0zw%2BqWFwRUoQ8RjmXkTKcD94sk0bRz1F3shvA0NdxRvr5PqDy5FdTJx8WnSp8cZE2M8YqQ19kAWO9scaVogtpwCJxEuiCfzUftaRovHatAq1R%2F80LRf8VhmFhlZfg10Eq9lupYDRLfjjnvQJG4zKCtwx6VHA4kJuxhdat0lIIWBD1CZhcgsNDzCALrWxAaIjkWT2tRJ0B8w86h5JNZh5DvQfuLJ2m0D14kRKUYYubtACo4mIGcrzKc6yiLxWmZINlhasHcAEtoc5ZEgSKl4rGFaWNyNcIsypOIcKsNNN9OC4BJgkGFMd%2B3rIX2f3B8tre3pZRxtqq7VwAMFwY2gg6I1fS0rgd2ohBD5AQ2PIS6%2BMzWXpwCTQXuhvI7wKuKaRlh9xDAScR0jFC4GXenrXjQ%2B63Q65nfinvNsbXuQmpgrH8R31LUiyZqqEQ6Nk2wr52oADQD7g5%2BApuGOH2l7YU9vxPUy4aqp4vXWqr94EhruD7JWvNZGu50nLyVW83ydi0oyT6dT4wqRGHKzL%2FUU1TFm6NurSYDcLPmmenZXJntTJdeYfW4F5D%2BFfIk3uiHuDgAAAABJRU5ErkJggg%3D%3D%2CMacIntel.1920.1080.24; wft=1; crtg_rta=criteo_250x250crtnative3criteo_200x200_Pins%3Bcriteo_200x200_Search%3B; _cnzz_CV1256903590=is-logon%7Clogged-out%7C1490170334892; _ga=GA1.2.659722060.1489734116; __asc=c44c6e9615af4faa683f624a6bd; __auc=4426e80715adb12a228b727e1b4; sid=LpKUX2dYDSQobYImEL6VqeAkafp.Ye41ttTXInOv21reRwzXRyhebcGzTKkgn%2FlSWI2yYEw; CNZZDATA1256903590=449876967-1489731133-null%7C1490168535',
			'Host':'huaban.com',
			'Pragma':'no-cache',
			'Referer':'http://huaban.com/favorite/pets/',
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
			'X-Request':'JSON',
			'X-Requested-With':'XMLHttpRequest'
}

def get_image_urls(url):
	response = requests.get(url,headers=headers)
	response.encoding= "utf-8"
	jsonObj = response.json()
	pins = jsonObj["pins"]
	for x in xrange(len(pins)):
		url = "http://img.hb.aicdn.com/"+pins[x]["file"]["key"]
		write_txt(url)
		print url
	next_url_id=pins[-1]['pin_id']
	print next_url_id
	next_page_url = make_next_request_url(next_url_id)
	print next_page_url
	get_image_urls(next_page_url)

def make_next_request_url(id_num):
	return "http://huaban.com/favorite/travel_places/?j0x9q48g&max=" + str(id_num) + "&limit=20&wfl=1"

def write_txt(url):
    try:
        if os.path.isfile(save_result_path)==False:
            os.system("touch "+save_result_path) 
        f= open(save_result_path,'a+')
        f.write(url.encode("utf-8"))
        f.write('\n')
    except Exception, e:
        print e
    finally:
        pass



get_image_urls(main_page)


