# url = 'http://www.mzitu.com/all/'
from bs4 import BeautifulSoup
import os
import re
import requests



def detail_img(page_url,ul_a_name_path):
    '''得到图片'''
    html_text = requests.get(page_url).text  # 获取文本内容
    soup = BeautifulSoup(html_text, 'lxml')
    div_a_src=soup.select('.main-image img')[0]['src']  # 得到图片的地址 http://i.meizitu.net/2018/08/05b01.jpg
    file_name=div_a_src.split('/')[-1]
    file_name=os.path.join(ul_a_name_path,file_name)  # 得到文件路径名

    headers={
        'Referer':page_url,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }

    with open(file_name,'wb') as f:
        img=requests.get(div_a_src,headers=headers).content
        f.write(img)





def detail_page_url(ul_a_href_list,ul_a_name_path):  # page详情页的url
    '''获得每一页的url'''
    html_text = requests.get(ul_a_href_list).text  # 获取文本内容
    soup = BeautifulSoup(html_text, 'lxml')
    div_a_page=soup.select('.pagenavi a span, .pagenavi-cm a')[-2].get_text()  # 最后一张图的数字
    for i in range(1,int(div_a_page)+1):
        page_url=f'{ul_a_href_list}/{i}' # 每一页的url
        detail_img(page_url,ul_a_name_path)


def total_catalog_url(url,path):  # 总目录的url
    '''获得每个目录下的url'''
    html_text=requests.get(url).text  # 获取文本内容
    soup=BeautifulSoup(html_text,'lxml')
    ul_a_list= soup.find('ul',class_='archives').find('p',class_='url').find_all('a') # 所有的a标签
    os.makedirs(path,exist_ok=True)
    for ul_a in ul_a_list:
        ul_a_name=ul_a.get_text()  # 得到a标签里的文本
        ul_a_name=re.sub('[\s，,:？?]','',ul_a_name) # 去除符号 只留下纯文本
        ul_a_name_path=os.path.join(path,ul_a_name)  # 存放路径
        os.makedirs(ul_a_name_path,exist_ok=True)  # 创建文件夹 meizitu/fafaef
        print(f'正在下载{ul_a_name_path}的图片')
        ul_a_href_list=ul_a.get('href')  # 获得链接地址
        detail_page_url(ul_a_href_list,ul_a_name_path)



def main():
    url = 'http://www.mzitu.com/all/'
    path = 'meizitu'
    total_catalog_url(url,path)


if __name__ == '__main__':
    main()
