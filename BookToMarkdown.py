#!/usr/bin/env python
#encoding:utf-8
import sys
import getopt
import os
import urllib.request
import urllib.parse
import requests
from pprint import pprint

DoubanBookApi = 'https://api.douban.com/v2/book/search?count={}&q={}'
QueryCount = 1
OutputFile = ''

def generateMarkdown(jsonData):
    if os.path.isabs(OutputFile):
        print("abs")
    else:
        print("not abs")

def requestData(url):
    r = requests.get(url)
    # pprint(r.json())

def getBookNames(argv):
    inputfile = ''
    bookNames = []
    global OutputFile
    global QueryCount

    try:
        opts, args = getopt.getopt(argv,"hi:o:c:",["ifile=","ofile=","count="])
    except getopt.GetoptError:
        print('usage: BookToMarkdown.py (-i bookNames.json | bookName) -o output.md [-c]')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('usage: BookToMarkdown.py (-i bookNames.json | bookName) -o output.md [-c]')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            OutputFile = arg
        elif opt in ("-c", "--count"):
            QueryCount = arg

    print('输入的文件为:', inputfile)
    print('输出的文件为:', OutputFile)
    print('count为：', QueryCount)

    if inputfile == '':
        bookNames = args
    else:
        bookNames = []

    return bookNames

def main(argv):
    bookNames = getBookNames(argv)
    for bookName in bookNames:
        url = DoubanBookApi.format(QueryCount, bookName)
        print("url is: ", url)
        data = requestData(url)
        generateMarkdown(data)



if __name__ == "__main__":
    main(sys.argv[1:])