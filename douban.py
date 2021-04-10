#encoding:utf-8
import urllib.request
import urllib.error
import re
import ffmpy
import os
from bs4 import BeautifulSoup
import requests
url='https://www.douban.com/search?cat=1001&q=%E8%BF%BD%E9%A3%8E%E7%AD%9D%E7%9A%84%E4%BA%BA'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}


def getHtmlData(url):
    print(url)
    # 欺骗为 iPhone/iPad 的请求
    req = urllib.request.Request(
        url,
        data = None,
        headers = header
        )
    try: 
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(e)
        return
    
    data = response.read()

    # 渲染回包数据
    bs = BeautifulSoup(data, 'html.parser')

    print(bs)

    return bs

def getBooksInfo(name):
    bs = getHtmlData(url) 

    # 过滤地址为404、503等的网页
    if bs == None:
        return

    bookResults = bs.find(class_= "result-list").find_all(class_='result')

    for result in bookResults:
        
        title = result.find(class_='content').find(class_='title').find('h3').find('a')
        print(title.string.strip())


    print(bookList)

getBooksInfo("1")
