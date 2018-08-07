# http://www.mm131.com/mingxing
import requests
import re
import os
from bs4 import BeautifulSoup

def detail_img(page_url, url_dd_name_list_path):
    '''得到图片'''
    html_text = requests.get(page_url).content.decode('gbk')
    soup = BeautifulSoup(html_text, 'lxml')
    img_src=soup.select('.content-pic img')[0]['src']  # 图片的地址
    file_name=img_src.split('/')[-1]
    file_name=os.path.join(url_dd_name_list_path,file_name)

    headers={
        'Referer':'http://www.mm131.com/mingxing/2016.html',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }


    with open(file_name,'wb') as f:
        img=requests.get(img_src,headers=headers).content  # 得到内容
        f.write(img)



def detail_page_url(url_dd_href_list,url_dd_name_list_path):
    '''详情页的url'''
    html_text = requests.get(url_dd_href_list).content.decode('gbk')
    soup = BeautifulSoup(html_text, 'lxml')
    # 得到页数
    div_a_page_max=soup.select('.content-page .page-en')[-1].get_text()  # 列表最后一个的文字 最大数字
    div_a_page_list = soup.select('.content-page .page-en')  # 得到所有a标签
    # 每一页的url
    for i in range(1,int(div_a_page_max)+1):
        if i==1:
            # http://www.mm131.com/mingxing/2016.html
            page_url=url_dd_href_list
            detail_img(page_url, url_dd_name_list_path)
        else:
            # http://www.mm131.com/mingxing/2016_2.html
            page_url='http://www.mm131.com/mingxing/'+div_a_page_list[i-2].get('href')
            detail_img(page_url, url_dd_name_list_path)



def total_catalog_url(url,path):
    '''得到总目录里所有的url'''
    html_text=requests.get(url).content.decode('gbk')
    soup=BeautifulSoup(html_text,'lxml')
    # 获得a标签
    url_dd_list=soup.find('div',class_='main').find('dl',class_='list-left public-box').find_all('a',target='_blank')
    os.makedirs(path,exist_ok=True)
    for url_dd in url_dd_list:
        url_dd_href_list=url_dd.get('href') # 每个目录下的url http://www.mm131.com/mingxing/2016.html
        url_dd_name_list=url_dd.get_text()  # 获取文本名
        url_dd_name_list_path=os.path.join(path,url_dd_name_list)  # 设置路径
        os.makedirs(url_dd_name_list_path,exist_ok=True)  # 创建文件夹
        print(f'正在下载{url_dd_name_list}的图片')
        detail_page_url(url_dd_href_list,url_dd_name_list_path)
    print('下载完毕')



def main():
    url='http://www.mm131.com/mingxing'
    path='mingxing'
    total_catalog_url(url,path)


if __name__ == '__main__':
    main()