# -*- coding: utf-8 -*-
import scrapy
from qczj_pro.items import QczjProItem

class QczjSpider(scrapy.Spider):
    name = 'qczj'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/4764.html#pvareaid=3454438']
    url='https://car.autohome.com.cn/pic/series/4764.html#pvareaid=3454438'

    def parse(self, response):
        car_names=response.xpath("//div[@class='uibox']/div[@class='uibox-title']/a[1]/text()").getall()[1:-1]
        for i in range(len(car_names)):
            car_name=car_names[i]
            car_imgs_urls=response.xpath("//div[@class='uibox'][{}]/div[@class='uibox-con carpic-list03']"
                                   "/ul/li/a/img/@src".format(str(i+2))).getall()
            car_imgs_urls=["https:"+car_imgs_url for car_imgs_url in car_imgs_urls]
            item=QczjProItem(car_name=car_name,car_imgs_urls=car_imgs_urls)
            yield item


