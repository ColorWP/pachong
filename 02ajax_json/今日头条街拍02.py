from bs4 import BeautifulSoup
from urllib.parse import urlencode
import requests
import os
import json
import re
from multiprocessing import Pool


MONGO_URL="localhost"  # 链接地址
MONGO_DB="toutiao"  # 数据库名称
MONGO_TABLE="toutiao"  # 表名

# client=pymongo.MongoClient(MONGO_URL)
# db=client[MONGO_DB]  # 数据库名称传递过去

# def save_to_mongo(result):
#     if db[MONGO_TABLE].insert(result):  # 是否导入进去
#         print('存储到MongoDB成功',result)
#         return True
#     return False


def main_next(GROUP_START,GROUP_END):
    keyword='街拍'
    path='今日头条街拍图集'

    for i in range(GROUP_START,GROUP_END):
        offset=i*20
        path = os.path.join(path,str(offset))
        os.makedirs(path, exist_ok=True)

        index_html = get_index_page(offset, keyword, path)

        detaile_name_html_list = parse_page_index(index_html, path)
        # print(detaile_name_html_list)

        for detail_name, detail_html in detaile_name_html_list.items():
            html = get_page_detail(detail_html)  # 得到url后 进入到详情页进行
            if html:
                print('正在下载：' + detail_name)
                image_list = parse_page_detail(html)
                # print(image_list)
                # save_to_mongo(image_list)
                download_image(image_list, detail_name)
        print('下载完成')



def get_index_page(offset,keyword,path):
    '''得到主页的json数据'''
    data={
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from': 'gallery'
    }
    url='https://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response=requests.get(url)
        if response:
            os.makedirs(path, exist_ok=True)  # 创建文件夹
            return response.text
        else:
            print('主页response为空',url)
            return None
    except Exception as e:
        print('主页获取url错误',url)



def parse_page_index(html,path):
    '''解析json数据'''
    # 对json字符串 转换成json格式的变量
    data=json.loads(html)  # load列表  loads字典
    detaile_name_html_list={} # 定义一个空的字典  用于存放每一个name:html
    if 'data' in data.keys():
        for i in data['data']:
            index_name=i.get('title')
            index_name = re.sub('[\s，？：！]', '',index_name)
            index_name=os.path.join(path,index_name)
            os.makedirs(index_name,exist_ok=True)   # 文件夹名 今日头条街拍图集/xxx

            detaile_name_html_list[index_name]=i.get('article_url')   # name:html
    # print(detaile_name_html_list)
    return detaile_name_html_list



def get_page_detail(detail_html):
    '''得到详情页的信息'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    try:
        response=requests.get(detail_html,headers=headers)
        if response:
            # print(response.text)
            return response.text
        else:
            print('详情页response为空',detail_html)
            return None
    except Exception as e:
        print('详情页获取url错误',detail_html)



def parse_page_detail(html):
    '''解析详情页信息'''
    js_str = re.findall("JSON\.parse\(\"(.*)\"\),", html)[0]
    # print(js_str)
    js_str = re.sub(r"\\", '', js_str)
    js_obj = json.loads(js_str)   # 得到最终的字符串
    # print(js_obj['sub_images'])
    image_list=[i.get('url') for i in js_obj['sub_images']]   # 得到图片所有的链接
    return image_list

def download_image(image_list,detail_name):
    for image_url in image_list:
        print(image_url)
        file_name = image_url.split('/')[-1]+'.jpg'
        file_name = os.path.join(detail_name, file_name)  # 得到文件路径名
        with open(file_name,'wb') as f:
            image=requests.get(image_url).content
            f.write(image)



def main():
    GROUP_START=0
    GROUP_END=20
    pool=Pool()
    # main_next(GROUP_START,GROUP_END)
    pool.apply_async(main_next, (GROUP_START, GROUP_END))  # 第一个参数是函数名  对象 ，第二个是参数
    pool.close()  # 关掉进程
    pool.join()  # 等待执行完成



if __name__ == '__main__':
    main()




