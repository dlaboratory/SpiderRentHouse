# -*- Coding = UTF-8 -*-
# Author: Nico
# File: spider_rent_house.py
# Software: PyCharm
# Time: 2024/1/20 15:35


import re
import time
import urllib.error
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup


def main():
    baseurl = 'https://bj.lianjia.com/zufang/chaoyang/pg'
    columns = ['小区', '区域', '面积', '价格', '朝向', '户型', '详情链接']
    # 创建DataFrame
    all_data = pd.DataFrame(columns=columns)
    for i in range(1, 100):
        print(f'正在爬取第{i}页数据...')
        time.sleep(1)
        url = baseurl + str(i)
        datalist = getdata(url)
        if not datalist:
            print(f'第{i}页数据为空，爬取结束！')
            break
        df = pd.DataFrame(datalist, columns=columns)
        # 将当前页数据追加到总的数据中
        all_data = all_data.append(df, ignore_index=True)
    # 将所有数据保存到一个Excel文件
    all_data.to_excel('data_rent_house.xlsx', index=False)
    print('爬取完毕！')


# 定义正则表达式
findname0 = re.compile(r' title="(.*?)">', re.S)
findname1 = re.compile(r'.html" target="_blank">\n          (.*?)        </a>', re.S)
findposition = re.compile(r'</a>-<a href=".*target="_blank">(.*?)</a>-', re.S)
findsize = re.compile(r'<i>/</i>(.*?)<i>/</i>', re.S)
findprice = re.compile(r'<em>(.*?)</em> (.*?)</span>', re.S)
findorientation = re.compile(r'        <i>/</i>(.*?)        <i>/</i>', re.S)
findlayout0 = re.compile(r'        <i>/</i>.*        <i>/</i>(.*?)        <span', re.S)
findlayout1 = re.compile(r'        <i>/</i>\n        (.*?)      </p>', re.S)
findlink0 = re.compile(r'<a class="twoline" href="(.*?)" target="_blank">', re.S)
findlink1 = re.compile(r'<a href="/apartment/(.*?).html" target="_blank">', re.S)


def getdata(url):
    datalist = []
    html = askurl(url)
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all('div', class_='content__list--item--main'):
        data = []
        item = str(item)
        try:
            # 使用正则表达式提取信息
            name = re.findall(findname0, item)[0]
            data.append(name)
            position = re.findall(findposition, item)[0]
            data.append(position)
            size = re.findall(findsize, item)[0]
            data.append(size.strip())
            price = re.findall(findprice, item)[0]
            price = f'{price[0]}{price[1]}'
            data.append(price)
            orientation = re.findall(findorientation, item)[0]
            data.append(orientation)
            layout = re.findall(findlayout0, item)[0]
            data.append(layout.strip())
            link = 'https://sh.lianjia.com' + re.findall(findlink0, item)[0]
            data.append(link)
        except:
            # 如果正则表达式未匹配，则使用备用的正则表达式进行匹配
            area = re.findall(findname1, item)[0]
            data.append(area)
            position = ''
            data.append(position)
            size = re.findall(findsize, item)[0]
            data.append(size.strip())
            price = re.findall(findprice, item)[0]
            price = f'{price[0]}{price[1]}'
            data.append(price)
            orientation = re.findall(findorientation, item)[0]
            data.append(orientation)
            layout = re.findall(findlayout1, item)[0]
            data.append(layout.strip())
            link = 'https://sh.lianjia.com/apartment/' + re.findall(findlink1, item)[0] + '.html'
            data.append(link)
        datalist.append(data)
    return datalist


def askurl(url):
    head = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 99.0.4844.51Safari / 537.36'
    }
    request = urllib.request.Request(url, headers=head)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    return html


if __name__ == '__main__':
    main()
