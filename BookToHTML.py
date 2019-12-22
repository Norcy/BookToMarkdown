#!/usr/bin/env python
#encoding:utf-8
import sys
import getopt
import os
import urllib.request
import urllib.parse
import requests
import json
from pprint import pprint
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape

DoubanBookNameApi = 'https://api.douban.com/v2/book/search?apikey=0df993c66c0c636e29ecbb5344252a4a&count={}&q={}'
DoubanBookIdApi = 'https://api.douban.com/v2/book/{}?apikey=0df993c66c0c636e29ecbb5344252a4a'
# DoubanBookUserApi = 'https://api.douban.com/v2/book/user/39646385/collections?count=101'
QueryCount = 1
OutputFile = 'book.html'
QueryById = False

def generateHTML(originBooks):
    env = Environment(
        loader=FileSystemLoader(""),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template("template.html")
    
    # pprint(originBooks)
    books=[];
    for book in originBooks:
        # pprint(book)
        books.append({'title':book['title'], 'subtitle': '', 'image': book['image'], 'time': book['myTime']})
    with open(OutputFile, 'w') as f:
        f.write(template.render(books=books, mainTitle="2020's Reading Challenge"))

def requestData(url):
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    headers={"User-Agent":user_agent}
    r = requests.get(url, headers=headers)
    # pprint(r.json())
    return r.json();

def printUsage():
    print('usage: BookToMarkdown.py (-i | -n) -o output.md [-c]')

def getBookInfos(argv):
    inputfile = ''
    bookInfos = []
    global OutputFile
    global QueryCount
    global QueryById

    try:
        opts, args = getopt.getopt(argv,"hn:i:o:c:",["name=", "ifile=","ofile=","count=","id"])
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            printUsage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        # elif opt in ("-o", "--ofile"):
        #     OutputFile = arg
        elif opt in ("-c", "--count"):
            QueryCount = arg
        elif opt in ("-n", "--name"):
            bookNames = [arg]
        elif opt in ("--id"):
            QueryById = True

    if inputfile != '':
        with open(inputfile, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    bookInfo = {}
                    lineInfo = line.split(' ');
                    bookInfo["myTime"] = lineInfo[0]
                    bookInfo["name"] = lineInfo[1]
                    bookInfos.append(bookInfo)

    if os.path.isabs(OutputFile) == False:
        OutputFile = os.getcwd()+"/"+OutputFile;

    if os.path.exists(OutputFile):
        os.remove(OutputFile)

    print('输入的文件为:', inputfile)
    print('输出的文件为:', OutputFile)
    print('count为:', QueryCount)
    print('bookInfos:', bookInfos)

    return bookInfos

def generateUrlByName(bookName):
    if QueryById == True:
        url = DoubanBookIdApi.format(bookName)
    else:
        url = DoubanBookNameApi.format(QueryCount, bookName)
    print("url is:", url)
    return url

def main(argv):
    bookInfos = getBookInfos(argv)
    datas = []
    for bookInfo in bookInfos:
        url = generateUrlByName(bookInfo["name"])
        data = requestData(url)
        singleData = {};
        if QueryById:
            singleData = data;
        else:
            singleData = data["books"][0]
        singleData["myTime"] = bookInfo["myTime"]
        datas.append(singleData)
        
    generateHTML(datas)

    os.system("open {}".format(OutputFile))

if __name__ == "__main__":
    main(sys.argv[1:])