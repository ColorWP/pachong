# coding = utf-8
# https://www.enterdesk.com/search/1-328-6-0-1920x1080-0/

from bs4 import BeautifulSoup
import os
import re
import requests


def total_img(a_href_url,img_url_path):
    '''所有的图片'''
    html_text = requests.get(a_href_url).text
    soup = BeautifulSoup(html_text, 'lxml')
    try:
        img_src=soup.find('div',class_='dowm_arc').find_all('img')  # 得到img标签
        # https://up.enterdesk.com/edpic_source/21/c0/b5/21c0b59aa2d3d42a7508cf9581c4e1a0.jpg
        img_src=img_src[0]['src']
        print(img_src)
        file_name=img_src.split('/')[-1]   # 21c0b59aa2d3d42a7508cf9581c4e1a0.jpg  得到名字
        file_name_path=os.path.join(img_url_path,file_name)

        with open(file_name_path,'wb') as f:
            get_img=requests.get(img_src).content
            f.write(get_img)
    except Exception as e:
        print(e)



def high_img_url(url_href,img_url_path):
    '''得到每一页原图高清url'''
    html_text = requests.get(url_href).text
    soup = BeautifulSoup(html_text, 'lxml')
    try:
        url=soup.find('div',class_='images_contrl').find_all('a') # 得到a标签
        a_href_url='https:'+url[0].get('href')   # //www.enterdesk.com/download/31978-198723/
        total_img(a_href_url, img_url_path)
    except Exception as e:
        print(e)


def secondary_page_url(img_url_href,img_url_path):
    '''次目录下，每一页的url'''
    html_text=requests.get(img_url_href).text
    soup=BeautifulSoup(html_text,'lxml')
    try:
        page_max=soup.find('div',class_='arc_pandn').find('div',class_='swiper-wrapper').find_all('a') # 得到所有的a标签
        img_url_href='/'.join(img_url_href.split('/')[0:3])  # https://mm.enterdesk.com
        # print(img_url_href)
        for page_href in page_max:
            # https://mm.enterdesk.com/bizhi/31978-198724.html
            url_href=img_url_href+page_href.get('href')  # 得到每张图片的href链接
            high_img_url(url_href,img_url_path)
    except Exception as e:
        print(e)



def secondary_catalog_url(page_url,url_catalog_path):
    '''大目录下所有的，每个次目录的url'''
    html_text=requests.get(page_url).text
    soup=BeautifulSoup(html_text,'lxml')
    img_url_list=soup.select('.egeli_pic_dl dt a') # 得到所有a标签
    for img_url in img_url_list:
        img_url_name=img_url.get_text()  # 得到文本内容
        img_url_name = re.sub('[\s,]', '', img_url_name)  # 删除 空格 及 ，
        img_url_href=img_url.get('href')  # https://mm.enterdesk.com/bizhi/31947.html
        # print(img_url_href)
        img_url_path=os.path.join(url_catalog_path,img_url_name)
        os.makedirs(img_url_path,exist_ok=True)
        print(img_url_name)
        secondary_page_url(img_url_href,img_url_path)


def primary_page_url(url_catalog_href,url_catalog_path):
    '''每个大目录下，每一页的url'''
    html_text=requests.get(url_catalog_href).text
    soup=BeautifulSoup(html_text,'lxml')
    # 得到a标签  <a href="https://www.enterdesk.com/search/2-328-6-0-1920x1080-0">2</a>
    detail_page_url_list=soup.select('.listpages ul li a')  # 找到所有a标签
    if detail_page_url_list==[]:
        detail_page_max=1
    else:
        detail_page_max=soup.select('.listpages ul li a')[-1].get('href')
        detail_page_max=detail_page_max.split('/')[-1].split('-')[0]  # 得到最大页数
    # 拼接
    x1 = '/'.join(url_catalog_href.split('/')[0:4])        # https://www.enterdesk.com/search
    x2 = (url_catalog_href.split('/')[-2].split('-')[0])   # 2-45-6-0-1920x1080-0  第一个数字
    for i in range(3,int(detail_page_max)+1):
        x3 = (url_catalog_href.split('/')[-2].split('-')[1::1])  # ['45', '6', '0', '1920x1080', '0']
        x2=f'{i}'
        x3.insert(0,x2)  # list插入到第一个位置
        x3='-'.join(x3)  # 拼接
        page_url=x1+'/'+x3   # 得到url
        url_catalog_path1=os.path.join(url_catalog_path,str(i))
        os.makedirs(url_catalog_path1,exist_ok=True)
        print(f'第{i}页')
        secondary_catalog_url(page_url, url_catalog_path1)



def primary_catalog_url(url,path):
    '''获得主页中，每个大目录下的url'''
    html_text=requests.get(url).text
    soup=BeautifulSoup(html_text,'lxml')
    url_catalog_list=soup.select('.list_sel_box ul a')[8:9] # 得到目录下的a标签
    os.makedirs(path,exist_ok=True)
    for url_catalog_href_list in url_catalog_list:
        url_catalog_href=url_catalog_href_list.get('href')  #  得到url  /search/1-45-6-0-1920x1080-0/
        url_catalog_href='https://www.enterdesk.com'+url_catalog_href
        url_catalog_name=url_catalog_href_list.get_text()  #  得到文本内容
        url_catalog_path=os.path.join(path,url_catalog_name)
        os.makedirs(url_catalog_path,exist_ok=True)
        print(f'正在下载 {url_catalog_name} 下的图片')
        primary_page_url(url_catalog_href,url_catalog_path)
    print('下载完毕')


def main():
    url='https://www.enterdesk.com/search/1-26-6-0-1920x1080-0/'
    path='bizhi03'
    primary_catalog_url(url,path)



if __name__ == '__main__':
    main()

#                               1 2 3 ...       大陆...欧美
#               [1,2,3...]   [1,2,3...]   [1,2,3...]   有多少页
#        [[1,2,3...],[1,2,3...],[]]    每个图片集
#     [[[1,2,3...],[],[]]]      # 图片集下  所有的页
#    最后的到图片
