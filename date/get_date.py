#coding: utf-8
import requests
import json
import time
import csv
import math
import codecs
import gaosi as gs


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


def millerToXY(lon, lat):
    """
    :param lon: 经度
    :param lat: 维度
    :return:
    """
    xy_coordinate = []
    L = 6381372 * math.pi * 2  # 地球周长
    W = L  # 平面展开，将周长视为X轴
    H = L / 2  # Y轴约等于周长一般
    mill = 2.3  # 米勒投影中的一个常数，范围大约在正负2.3之间
    x = lon * math.pi / 180  # 将经度从度数转换为弧度
    y = lat * math.pi / 180
    # 将纬度从度数转换为弧度
    print("mark")
    y1 = y
    print(math.tan(0.25 * math.pi + 0.4 * y1))
    y = 1.25 * math.log(math.tan(0.25 * math.pi + 0.4 * y1))  # 这里是米勒投影的转换

    print("mark")
    # 这里将弧度转为实际距离 ，转换结果的单位是公里
    x = (W / 2) + (W / (2 * math.pi)) * x
    y = (H / 2) - (H / (2 * mill)) * y
    xy_coordinate.append(x, y)
    print("mark")
    return xy_coordinate

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
                    _lat = float(r['location']['lat'])
                    _lng = float(r['location']['lng'])
                    x = gs.LB_to_xy(_lat, _lng)
                    writer.writerow([str(count),city_area, _name, x[0], x[1]])
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