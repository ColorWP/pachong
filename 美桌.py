# coding = utf-8

import requests
import os
from bs4 import BeautifulSoup
from multiprocessing import Pool



def detail(img_href_new,total_img_name):
    html_text=requests.get(img_href_new).text
    soup=BeautifulSoup(html_text,'lxml')
    href_list=soup.select('#picBox > ul > li')
    for a_href in href_list:
        href=a_href.find('a').get('href')
        print(href)
        href_name=href.split('/')[-1]
        file_name=os.path.join(total_img_name,href_name)

        with open(file_name,'wb') as f:
            img=requests.get(href).content
            f.write(img)




def index_img(page_url,page_name):
    html_text=requests.get(page_url).text
    soup=BeautifulSoup(html_text,'lxml')
    total_img=soup.select('.Left_list_cont .tab_box ul li a') # 得到所有a
    for img_href_list in total_img:
        img_href=img_href_list.get('href')
        img_title=img_href_list.get('title')
        print(img_title)
        total_img_name=os.path.join(page_name,img_title)
        os.makedirs(total_img_name,exist_ok=True)

        img_href_header=img_href.split('_')[0]
        img_href_footer=img_href.split('_')[-1]
        # http://www.win4000.com/wallpaper_detail_149085.html
        # http://www.win4000.com/wallpaper_big_148998.html
        img_href_new=f'{img_href_header}_big_{img_href_footer}'
        detail(img_href_new,total_img_name)



def index_page(url,path):
    html_text=requests.get(url).text
    soup=BeautifulSoup(html_text,'lxml')
    page_a_href=soup.select('.pages a')[-2::-1]  # 获取所有的a标标签
    page_a_href.append(url)  # 把第一页页加进去
    pool=Pool()
    for page_href in page_a_href:
        try:
            page_url=page_href.get('href')
        except Exception as e:
            page_url=url
        page_name = page_url.split('_')[-1].split('.')[0]  # 得到页码
        print(page_name)
        page_name=os.path.join(path,page_name)
        os.makedirs(page_name,exist_ok=True)
        index_img(page_url,page_name)
    pool.close()  # 关掉进程
    pool.join()  # 等待执行完成
    print('下载完成')

def main():
    url='http://www.win4000.com/wallpaper_2285_0_7_1.html'
    path='美桌'
    print('开始下载')
    index_page(url,path)

if __name__ == '__main__':
    main()