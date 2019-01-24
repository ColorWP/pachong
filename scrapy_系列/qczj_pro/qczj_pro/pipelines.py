# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from urllib import request


class QczjProPipeline(object):
    def __init__(self):
        # 创建车文件夹 存储
        image_path=os.path.dirname(os.path.dirname(__file__))
        self.images_all=os.path.join(image_path,'images_all')
        if not os.path.exists(self.images_all):
            os.mkdir(self.images_all)

    def process_item(self, item, spider):
        car_name=item['car_name']
        car_imgs_urls=item['car_imgs_urls']

        car_path=os.path.join(self.images_all,car_name)  # 车每一部分的文件夹
        if not os.path.exists(car_path):
            os.mkdir(car_path)

        for car_imgs_url in car_imgs_urls:
            print(car_imgs_url)
            car_imgs_name=car_imgs_url.split('_')[-1]  # 给图片起的名字
            car_imgs_path=os.path.join(car_path,car_imgs_name)  # 车具体的图片
            request.urlretrieve(car_imgs_url,car_imgs_path)

        return item



