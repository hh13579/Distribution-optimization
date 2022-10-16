#coding: utf-8
import requests
import json
import time
import csv
import codecs


"""
    查询关键字：
"""
FileKey = 'preclass'
KeyWord = u"小区"

def getBaiduApiAk():
    """
    获取配置文件中百度apikey:
     { "baiduak":"xx"}
    :return: str
    """
    return "ZURIMeTBF76H3ZyAUa66yENyiNOnQUwD"


def requestBaiduApi(keyWords, baiduAk, fileKey):
    today = time.strftime("%Y-%m-%d")
    pageNum = 0
    count = 0
    logfile = open("./" + fileKey + "-" + today + ".log", 'a+', encoding='utf-8')
    file = open("./" + fileKey + "-" + today + ".txt", 'a+', encoding='utf-8')

    file_csv = open('data_福田区.csv', 'w+', encoding='utf-8')  # 追加
    writer = csv.writer(file_csv)
    writer.writerow(["no","area","name","lat","lng"])

    # print('-------------')
    # print(index)
    while True:
        try:
            URL = "http://api.map.baidu.com/place/v2/search?query=" + keyWords + \
                "&region=" + "深圳市福田区" + \
                "&output=json" +  \
                "&ak=" + baiduAk + \
                "&scope=1" + \
                "&page_size=20" + \
                "&page_num=" + str(pageNum)
            # print(pageNum)
            print(URL)
            resp = requests.get(URL)
            res = json.loads(resp.text)
            # print(resp.text.strip())
            if len(res['results']) == 0:
                logfile.writelines(time.strftime("%Y%m%d%H%M%S") + " stop " + " " + str(pageNum) + '\n')
                break
            else:
                for r in res['results']:
                    # print(r)
                    count += 1
                    city_area = r['city']+r['area']
                    _name = r['name']
                    _lat = str(r['location']['lat'])
                    _lng = str(r['location']['lng'])
                    writer.writerow([str(count),city_area, _name, _lat, _lng])
                    # file.writelines(str(r).strip() + '\n')
                    # print(r['city']+r['area']+" "+r['name']+" "+str(r['location']['lat']) + " " + str(r['location']['lng']))
            pageNum += 1
            time.sleep(1)
        except:
            print("except")
            logfile.writelines(time.strftime("%Y%m%d%H%M%S") + " except " + " " + str(pageNum) + '\n')
            break
def main():
    baiduAk = getBaiduApiAk()
    requestBaiduApi(keyWords=KeyWord, baiduAk=baiduAk, fileKey=FileKey)

if __name__ == '__main__':
    main()