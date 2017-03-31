#### 花瓣爬虫简单说明

首先进入你要爬取的页面

我以http://huaban.com/favorite/travel_places/ 为例子

右键 “检查”，选择network, 往下滑动页面，这时候就会有网络请求，找到我们需要的请求

如 http://huaban.com/favorite/travel_places/?j0xapa21&max=1081611043&limit=20&wfl=1

![](http://oic2oders.bkt.clouddn.com/github_hua_ban_chrome_screen_cut.png)

然后复制下Response的结果，在 http://json.cn/ 里查看format后的结果，找到对应的数据。

```json
{
    "filter":"pin:category:travel_places",
    "pins":[
        {
            "pin_id":1081388818,
            "user_id":141402,
            "board_id":409091,
            "file_id":131759569,
            "file":{
                "id":131759569,
                "farm":"farm1",
                "bucket":"hbimg",
                "key":"cad3b3be27c98e222065f6a20bb2285d9c1d872d9e124-R3LxxT",
                "type":"image/jpeg",
                "width":"1024",
                "height":"683",
                "frames":"1",
                "colors":[
                    {
                        "color":14342874,
                        "ratio":0.1
                    }
                ],
                "audit":{
                    "porn":{
                        "rate":0.9999141809676075,
                        "label":0,
                        "review":false
                    }
                },
                "theme":"dadada"
            },
            "media_type":0,
            "source":"nipic.com",
            "link":"http://www.nipic.com/show/16746237.html?v=2",
            "raw_text":"新疆喀纳斯湖 喀纳斯景区 旅游观光胜地 峡谷中的湖 内陆淡水湖 山峦起伏 植物树木 阿勒泰地区 人间仙境 高山湖泊 清澈湖水 变换颜色湖水 自然风光",
            "text_meta":{

            },
            "via":1043457819,
            "via_user_id":19710125,
            "original":1043457819,
            "created_at":1490868088,
            "like_count":0,
            "comment_count":0,
            "repin_count":1,
            "is_private":0,
            "orig_source":null,
            "user":{
                "user_id":141402,
                "username":"休纱",
                "urlname":"wangheady",
                "created_at":1332149742,
                "avatar":{
                    "id":74814335,
                    "farm":"farm1",
                    "bucket":"hbimg",
                    "key":"dee8c814cd883df97eadaf34cc416847ef42b7403fbf-viFpjv",
                    "type":"image/jpeg",
                    "width":408,
                    "height":408,
                    "frames":1
                },
                "extra":null
            },
            "board":{
                "board_id":409091,
                "user_id":141402,
                "title":"旅行",
                "description":"",
                "category_id":"travel_places",
                "seq":1,
                "pin_count":972,
                "follow_count":42,
                "like_count":0,
                "created_at":1332149777,
                "updated_at":1490868097,
                "deleting":0,
                "is_private":0,
                "extra":null
            },
            "via_user":{
                "user_id":19710125,
                "username":"六王爷",
                "urlname":"znl21",
                "created_at":1479094868,
                "avatar":{
                    "bucket":"hbimg",
                    "farm":"farm1",
                    "frames":1,
                    "height":300,
                    "id":102890808,
                    "key":"654953460733026a7ef6e101404055627ad51784a95c-B6OFs4",
                    "type":"image/jpeg",
                    "width":300
                },
                "extra":null
            }
        }
    ],
    "explore":null,
    "promotions":null,
    "suggests":{

    },
    "banner_box_promotion":null,
    "query":null
}
```

这里选取了返回的20个结果的一个作为示例，pins对应的JsonArray的最后一个，找到Key为pin_id作为下一次请求的max对应的值。每个图片的地址为  "http://img.hb.aicdn.com/"+pins里的"file"中的"key"。