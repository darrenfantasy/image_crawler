#encoding:utf-8
import MySQLdb as mdb
import sys
import json
con = None

json_path = "douban_donghua_results.txt"
def get_jsonarray_from_txt(path):
  try:
    f = open(path,"r")
    text = f.read()
    array = json.loads(text)
    print len(array)
    f.close()
    return array
  except Exception, e:
    print e
  finally:
    pass

try:
  #连接 mysql 的方法： connect('ip','user','password','dbname')
  con = mdb.connect('localhost', 'root','root', 'test',charset="utf8");
 
  #所有的查询，都在连接 con 的一个模块 cursor 上面运行的
  cur = con.cursor()
 
  data = []
  json_array = get_jsonarray_from_txt(json_path)
  for x in xrange(len(json_array)):
    item = json_array[x]
    print item["directors_cn_names"]
    print ','.join(item["directors_cn_names"])
    # values = [item["subject_id"],item["movie_name"],item["directors_cn_names"],item["directors_en_names"],item["actors_cn_names"],item["actors_en_names"],item["genres"],item["tags"],item["languages"],item["average"],item["alternate_name"],item["countries"]]
    try:
      values = [item["subject_id"],item["movie_name"],','.join(item["directors_cn_names"]),','.join(item["directors_en_names"]),','.join(item["actors_cn_names"]),','.join(item["actors_en_names"]),','.join(item["genres"]),','.join(item["tags"]),','.join(item["languages"]),item["average"],','.join(item["alternate_name"]),','.join(item["countries"])]
      cur.execute('insert into douban_movie(subject_id,movie_name,directors_cn_names,directors_en_names,actors_cn_names,actors_en_names,genres,tags,languages,average,alternate_name,countries) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',values)
    except KeyError, e:
      print e
    finally:
      pass
  cur.close()
except Exception, e:
  print e
finally:
  if con:
    #无论如何，连接记得关闭
    con.commit()
    con.close()