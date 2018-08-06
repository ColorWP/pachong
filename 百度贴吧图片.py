import requests
from urllib.request import urlretrieve
import re

# <img pic_type="0" class="BDE_Image" src="https://imgsa.baidu.com/forum/w%3D580/sign=941c6a9596dda144da096cba82b6d009/e889d43f8794a4c2e5d529ad0ff41bd5ac6e3947.jpg" pic_ext="jpeg" height="350" width="560">

# 一

# def get_image(page):
#     try:
#         reg=r'src="(.+?\.jpg)" pic_ext'
#         image=re.compile(reg)
#         for i_page in range(1,page+1):
#             html = requests.get(url+'?pn=%s'%i_page).text   # 得到源代码
#             image_list=re.findall(image,html)
#             x=1
#             for i in image_list:
#                 urlretrieve(i,'./show/'+'%s-%s.jpg'%(i_page,x))
#                 x+=1
#     except Exception as e:
#         print(e)
#
# if __name__=='__main__':
#     url='http://tieba.baidu.com/p/2460150866'
#     page=3
#     get_image(page)
#     print('图片下载完成')



# 二

from bs4 import BeautifulSoup

def mk_url(url,page):   # 得到第page页的url
    url=url+'?pn=%s'%page
    return url

def get_html(url):    # 得到相应源代码
    try:
        a=requests.get(url)
        html=a.text
        return html
    except Exception as e:
        print(e)
        return None

# <img pic_type="0" class="BDE_Image" src="https://imgsa.baidu.com/forum/w%3D580/sign=941c6a9596dda144da096cba82b6d009/e889d43f8794a4c2e5d529ad0ff41bd5ac6e3947.jpg" pic_ext="jpeg" height="350" width="560">

def get_image(html,page):
    try:
        soup=BeautifulSoup(html,'lxml')  # 构造soup对象   源代码包装到soup  方便解析
        image_list=soup.find_all('img',class_="BDE_Image")
        x=1
        for i in image_list:
            img=i.get('src')
            name='./show/'+'%s-%s.jpg'%(page,x)
            urlretrieve(img,name)
            print(x)
            x+=1
    except Exception as e:
        print(e)

def main(url,page):
    for page_p in range(1,page+1):
        url_p=mk_url(url,page_p) # 调用第一个函数 得到url
        html_p=get_html(url_p)   # 调用第二个函数 得到html
        get_image(html_p,page_p) # 调用第三个函数 得到图片

if __name__=='__main__':
    url='http://tieba.baidu.com/p/2460150866'
    page=3   # 可修改
    main(url,page)
    print('图片下载完成')

