# coding = utf-8
# http://www.mm131.com/mingxing

import os
from multiprocessing import Pool  # 多进程
import requests
from bs4 import BeautifulSoup

def detail_img(girl_href_img,girl_name):
    html_text = requests.get(girl_href_img).content.decode('gbk')
    soup = BeautifulSoup(html_text, 'lxml')
    img_src=soup.select('.content-pic img')[0]['src']
    img_name=img_src.split('/')[-1]
    img_name=os.path.join(girl_name,img_name)
    print(img_src)

    headers={
        'Referer':'http://www.mm131.com/mingxing/1897.html',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    with open(img_name,'wb') as f:
        img=requests.get(img_src,headers=headers).content
        f.write(img)



def secondary_page_url(girl_href,girl_name):
    html_text = requests.get(girl_href).content.decode('gbk')
    soup = BeautifulSoup(html_text, 'lxml')
    max_page=int(soup.select('.content-page .page-ch')[0].get_text()[1:-1]) # 得到最大页数
    print(max_page)
    a_page_list = soup.select('.content-page .page-en') # 得到所有的a标签
    base_url=girl_href.split('.html')[0]  # http://www.mm131.com/mingxing/490
    for i in range(1,max_page+1):
        if i==1:
            girl_href_img=girl_href
        else:
            girl_href_img=f'{base_url}_{i}.html'
        detail_img(girl_href_img,girl_name)


def index_page_url(page_url,path):
    html_text = requests.get(page_url).content.decode('gbk')
    soup = BeautifulSoup(html_text, 'lxml')
    a_path_name = soup.select('.page .page_now')[0].get_text()  # 总目录下得到具体那一页的下标
    print(a_path_name)
    a_path_name=os.path.join(path,a_path_name)
    os.makedirs(a_path_name, exist_ok=True)  # 创建目录文件夹
    a_href_list=soup.select('.list-left dd')[:-1]  # 得到所有的a
    for second_url in a_href_list:
        girl_a=second_url.find('a')
        girl_href=girl_a.get('href') # 得到href
        girl_name=girl_a.get_text()  # 得到文本标题
        print(girl_name)
        girl_name=os.path.join(a_path_name, girl_name)
        os.makedirs(girl_name,exist_ok=True)
        secondary_page_url(girl_href,girl_name)



def total_index(url,path):
    html_text=requests.get(url).content.decode('gbk')
    soup=BeautifulSoup(html_text,'lxml')
    a_page_list = soup.select('.list-left .page')[0].find_all('a')
    # 得到每一页的href    [''http://www.mm131.com/mingxing/list_5_3.html', xxx]
    a_href_list=list(set(['{}/{}'.format(url,i.attrs['href']) for i in a_page_list]))
    a_href_list.append(url)  # 添加第一页
    os.makedirs(path, exist_ok=True)
    pool=Pool()  # 实例化
    for page_url in a_href_list:
        # index_page_url(page_url,path)
        pool.apply_async(index_page_url,(page_url,path)) # 第一个参数是函数名  对象 ，第二个是参数
    pool.close() # 关掉进程
    pool.join()   # 等待执行完成
    print('下载完成')




def main():
    url='http://www.mm131.com/mingxing'
    path='明星图'
    total_index(url,path)

if __name__ == '__main__':
    main()
