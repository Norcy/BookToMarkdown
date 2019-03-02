#!/usr/bin/env python
#encoding:utf-8
import sys
import getopt
import os
import urllib.request
import urllib.parse
import requests
from pprint import pprint

DoubanBookNameApi = 'https://api.douban.com/v2/book/search?count={}&q={}'
DoubanBookIdApi = 'https://api.douban.com/v2/book/{}'
# DoubanBookUserApi = 'https://api.douban.com/v2/book/user/39646385/collections?count=101'
QueryCount = 1
OutputFile = ''
QueryById = False

def generateMarkdown(jsonData):
    if QueryById:
        book = jsonData
    else:
        book = jsonData["books"][0]

    with open(OutputFile, 'a') as f:
        # Title
        f.write("## [{}]({})\n".format(book["title"], book["url"]));
        # Image
        f.write("<img src={} width='20%' height='20%'>\n".format(book["image"]));
        # Id
        # f.write("{}\n".format(book["id"]));
        # newLine
        f.write("\n")

def requestData(url):
    r = requests.get(url)
    # pprint(r.json())
    return r.json()

def printUsage():
    print('usage: BookToMarkdown.py (-i inputfile | -n bookName) -o output.md [-c]')

def getBookNames(argv):
    inputfile = ''
    bookNames = []
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
        elif opt in ("-o", "--ofile"):
            OutputFile = arg
        elif opt in ("-c", "--count"):
            QueryCount = arg
        elif opt in ("-n", "--name"):
            bookNames = [arg]
        elif opt in ("--id"):
            QueryById = True

    if inputfile != '':
        with open(inputfile, 'r') as f:
            for line in f.readlines():
                bookNames.append(line.strip())

    if os.path.isabs(OutputFile) == False:
        OutputFile = os.getcwd()+"/"+OutputFile;

    if os.path.exists(OutputFile):
        os.remove(OutputFile)

    print('输入的文件为:', inputfile)
    print('输出的文件为:', OutputFile)
    print('count为:', QueryCount)
    print('bookNames:', bookNames)

    return bookNames

def generateUrlByName(bookName):
    if QueryById == True:
        url = DoubanBookIdApi.format(bookName)
    else:
        url = DoubanBookNameApi.format(QueryCount, bookName)
    print("url is:", url)
    return url

def main(argv):
    bookNames = getBookNames(argv)
    for bookName in bookNames:
        url = generateUrlByName(bookName)
        data = requestData(url)
        generateMarkdown(data)

    os.system("open {}".format(OutputFile))

if __name__ == "__main__":
    main(sys.argv[1:])