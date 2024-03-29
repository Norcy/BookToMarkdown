#!/usr/bin/env python
#encoding:utf-8
import sys
import getopt
import os
import urllib.request
import urllib.parse
import requests
from pprint import pprint

DoubanMovieNameApi = 'https://api.douban.com/v2/movie/search?count={}&q={}'
DoubanMovieIdApi = 'https://api.douban.com/v2/movie/{}'

QueryCount = 1
OutputFile = ''
QueryById = False

def generateMarkdown(jsonData):
    if QueryById:
        movies = [jsonData]
    else:
        movies = jsonData["subjects"]

    with open(OutputFile, 'a') as f:
        for movie in movies:
            # Title
            f.write("## [{}]({})\n".format(movie["title"], movie["alt"]));
            # Image
            f.write("<img src={} width='20%' height='20%'>\n".format(movie["images"]["small"]));
            # Id
            # f.write("{}\n".format(movie["id"]));
            # newLine
            f.write("\n")

def requestData(url):
    r = requests.get(url)
    # pprint(r.json())
    return r.json()

def printUsage():
    print('usage: MovieToMarkdown.py (-i | -n) -o output.md [-c]')

def getMovieNames(argv):
    inputfile = ''
    movieNames = []
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
            movieNames = [arg]
        elif opt in ("--id"):
            QueryById = True

    if inputfile != '':
        with open(inputfile, 'r') as f:
            for line in f.readlines():
                movieNames.append(line.strip())

    if os.path.isabs(OutputFile) == False:
        OutputFile = os.getcwd()+"/"+OutputFile;

    if os.path.exists(OutputFile):
        os.remove(OutputFile)

    print('输入的文件为:', inputfile)
    print('输出的文件为:', OutputFile)
    print('count为:', QueryCount)
    print('movieNames:', movieNames)

    return movieNames

def generateUrlByName(movieName):
    if QueryById == True:
        url = DoubanMovieIdApi.format(movieName)
    else:
        url = DoubanMovieNameApi.format(QueryCount, movieName)
    print("url is:", url)
    return url

def main(argv):
    movieNames = getMovieNames(argv)
    for movieName in movieNames:
        url = generateUrlByName(movieName)
        data = requestData(url)
        generateMarkdown(data)

    os.system("open {}".format(OutputFile))

if __name__ == "__main__":
    main(sys.argv[1:])