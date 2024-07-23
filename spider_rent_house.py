# -*- Coding = UTF-8 -*-
# Author: Nico
# File: spider_rent_house.py
# Software: PyCharm
# Time: 2024/5/12 21:52


import time
import parsel
import random
import requests
import pandas as pd

URL_LISTS = {
    '北京朝阳': 'https://bj.lianjia.com/zufang/chaoyang/pg'
}


class SpiderRentHouse:
    def __init__(self):
        self.sleep_time = random.randint(1, 3)
        self.excel_path = 'data_rent_house.xlsx'
        self.href_head = 'https://sh.lianjia.com/'

    def spider_rent_house(self):
        data_list_rent_house = []
        for key, value in URL_LISTS.items():
            try:
                for page in range(1, 101):
                    print('-------------------------正在爬取{}第{}页租房数据-------------------------'.format(key, page))
                    time.sleep(self.sleep_time)
                    url = value + str(page)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
                    }
                    response = requests.get(url=url, headers=headers)
                    response.raise_for_status()
                    selector = parsel.Selector(response.text)
                    divs = selector.css('div.content__list--item--main')
                    if not divs:
                        break
                    for div in divs:
                        try:
                            area_list = div.css('.content__list--item--des a')
                            name = area_list[2].css('::text').get()
                            region = area_list[1].css('::text').get()
                            layout_list = div.css('.content__list--item--des i')
                            type_house = layout_list[2].xpath('following-sibling::text()').get().strip()
                            area = layout_list[0].xpath('following-sibling::text()').get().strip()
                            face = layout_list[1].xpath('following-sibling::text()').get().strip()
                            floor = layout_list[3].xpath('following-sibling::text()').get().strip().replace(
                                '                        ', '').replace('（', '(').replace('）', ')')
                            rent_price = div.css('span.content__list--item-price > em::text').get() + div.css(
                                'span.content__list--item-price::text').get().replace(' ', '')
                            href = self.href_head + div.css('.content__list--item--title a::attr(href)').get()
                            zone = key
                            data = {
                                'name': name,
                                'region': region,
                                'type_house': type_house,
                                'area': area,
                                'face': face,
                                'floor': floor,
                                'rent_price': rent_price,
                                'href': href,
                                'zone': zone
                            }
                            data_list_rent_house.append(data)
                        except Exception as e:
                            pass
            except Exception as e:
                print('爬取失败：{}'.format(e))
        df_data_list_rent_house = pd.DataFrame(data_list_rent_house)
        df_data_list_rent_house.to_excel(self.excel_path, index=False)
        print('租房数据爬取完毕！')

    def run(self):
        self.spider_rent_house()


if __name__ == '__main__':
    SpiderRentHouse().run()
