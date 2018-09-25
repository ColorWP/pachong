import re
import os
import requests
from urllib.parse import urlencode
from multiprocessing import Pool


def get_img_list(url_list, path,number):
    html_text=requests.get(url_list).text
    get_img=re.findall('wallpaper\"\s+src=\"(.*?)\"',html_text)[0]
    img_url='https:'+get_img
    name=f'{number}.'+img_url.split('.')[-1]
    name=os.path.join(path,name)
    print(img_url)

    with open(name,'wb') as f:
        img=requests.get(img_url).content
        f.write(img)


def first_index(page,path):
    data={'page':page}
    headers={
        'Referer':'https://alpha.wallhaven.cc/latest?page=1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    url = 'https://alpha.wallhaven.cc/latest?'+urlencode(data)
    try:
        html_text=requests.get(url,headers=headers).text
        get_url_list = re.findall("class=\"preview\" href=\"(.*?)\"\s+target", html_text)
        if get_url_list:
            path=os.path.join(path,str(page))
            os.makedirs(path,exist_ok=True)
            number=0   # 用于命名
            for url_list in get_url_list:
                number=number+1
                get_img_list(url_list, path,number)
        else:
            print('错误报告：未得到主页面url地址')
    except Exception as e:
        print(e)


def main():
    path='wallhaven_最新'
    pool=Pool()
    for page in range(1,2):
        print(f'正在下载第{page}页')
        pool.apply_async(first_index,(page,path))
    pool.close()
    pool.join()
    print('下载完成')




if __name__ == '__main__':
    main()
