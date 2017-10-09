# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json
import base64
import re
import time
import pandas as pd

time1=time.time()


###########模拟登录新浪
def login(username, password):
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    session = requests.Session()
    res = session.post(loginURL, data = postData)
    jsonStr = res.content.decode('gbk')
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        print(U"登录成功")
        # 把cookies添加到headers中，必须写这一步，否则后面调用API失败
        cookies = session.cookies.get_dict()
        cookies = [key + "=" + value for key, value in cookies.items()]
        cookies = "; ".join(cookies)
        session.headers["cookie"] = cookies
    else:
        print(U"登录失败，原因： %s" % info["reason"])
    return session


session = login('账号', '密码')
##################定义数据结构列表存储数据
top_name = []
url_new1=[]
url_new2=[]
pageids = []

#########################开始循环抓取
for i in range(1,5):
    try:
        print "正在抓取第"+str(i)+"页。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。"
        url2="http://d.weibo.com/100803?pids=Pl_Discover_Pt6Rank__5&cfs=920&Pl_Discover_Pt6Rank__5_filter=hothtlist_type=0&Pl_Discover_Pt6Rank__5_page="+str(i)+"&ajaxpagelet=1&__ref=/100803&_t=FM_149273744327929"
        html=session.get(url2).content

        ###########正则表达式匹配#######################
        name=re.findall("Pl_Discover_Pt6Rank__5(.*?)</script>",html,re.S)
        for each in name:
            # print each
            k=re.findall('"html":"(.*?)"}',each,re.S)
            # print each
            for each1 in k:
                k1=str(each1).replace('\\t',"").replace('\\n','').replace('\\','').replace('#','')
                # print k1
                k2=re.findall('alt="(.*?)" class="pic">',str(k1),re.S)
                for each2 in k2:
                    # print each2
                    top_name.append(each2)
                k3=re.findall('</span><a target="_blank" href="(.*?)" class="S_txt1"  >',str(k1),re.S)
                # print "k3Length:"
                # print len(k3)
                for x in xrange(len(k3)):
                    # print(k3[x])
                    newUrl = "https:"+k3[x].replace("?from=faxian_huati","/topic_album?from=page_100808&mod=TAB#place")
                    page_id = k3[x].lstrip("//weibo.com/p/").rstrip("?from=faxian_huati")
                    pageids .append(page_id)
                    url_new1.append(k3[x])
                    url_new2.append(newUrl)
    except:
        pass



apiUrl = "https://weibo.com/p/aj/proxy"
page_id = ""
page = 2
gifs = []
try:
    for x in xrange(5,15):
        print top_name[x]
        # print url_new1[x]
        # print url_new2[x]
        # print pageids[x]
        page_id = pageids[x]
        since_id = ""
        for y in xrange(30):
            time.sleep(1)
            page = y+2
            params = {"api":"http://i.huati.weibo.com/pcpage/papp","ajwvr":6,"atype":"all","viewer_uid":"1942763351","since_id":since_id,"page_id":page_id,"page":page,"ajax_call":1,"appname":"album","module":"feed","is_feed":1,"_rnd":"1506317976286"}
            html = session.get(apiUrl,params = params).content
            # print html
            k1=str(html).replace('\\t',"").replace('\\n','').replace('\\','').replace('#','')
            imgs=re.findall('<img class="photo_pict" src="(.*?)">',k1,re.S)
            for z in xrange(len(imgs)):
                if ".gif" in imgs[z]:
                    print imgs[z].replace("thumb300","large").replace("https","http")
                    gifs.append(imgs[z].replace("thumb300","large").replace("https","http"))
            since_ids = re.findall('action-data="(.*?)"',k1,re.S)
            selected_since_ids = []
            for i in xrange(len(since_ids)):
                if "since_id" in since_ids[i]:
                    selected_since_ids.append(since_ids[i])
            if len(selected_since_ids)>0:
                result_since_id = selected_since_ids[-1]
                # print result_since_id
                since_id = result_since_id[int(result_since_id.find("since_id="))+9:int(result_since_id.find("&isPrivate"))].replace("%23","#")
            else:
                break;
            # print since_id 
except Exception, e:
    print e
finally:
    pass





