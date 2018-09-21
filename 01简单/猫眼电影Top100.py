# 抓取猫眼电影Top100 相关信息

import requests
from bs4 import BeautifulSoup


def write_to_file(data):
    '''写入数据'''
    # 写的全是字符串格式
    with open('猫眼电影Top100.txt','a',encoding='utf-8') as f:
        f.write(str(data)+'\n')


def get_one_page(url):
    '''得到数据'''
    headers={
        'Referer': 'http://maoyan.com/board/4',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
       }
    html_text=requests.get(url,headers=headers).text
    soup=BeautifulSoup(html_text,'lxml')
    # print(soup)

    top=[i.get_text() for i in soup.select('.board-index')]
    image_url=[i['data-src'] for i in soup.select('.board-img')]
    title=[i['title'] for i in soup.select('.board-item-content .name a')]
    Lead=[i.get_text().replace(' ','').replace('\n','') for i in  soup.select('.board-item-content .star')]
    time= [i.get_text() for i in  soup.select('.board-item-content .releasetime')]
    score1= [i.get_text() for i in soup.select('.score-num .integer')]
    score2= [i.get_text() for i in soup.select('.score-num .fraction')]

    for i in range(10):
        data = {}
        data['top']=top[i]                  # 等级
        data['image_url']=image_url[i]      # 图片地址
        data['title']=title[i]              # 电影名
        data['Lead']=Lead[i]                # 主角
        data['time']=time[i]                # 上映时间
        data['score']=score1[i]+score2[i]   # 评分
        write_to_file(data)


def main():
    for i in range(10):
        offset=i*10
        url = f'http://maoyan.com/board/4?offset={offset}'
        print(f'第{i}页')
        get_one_page(url)


if __name__ == '__main__':
    main()
