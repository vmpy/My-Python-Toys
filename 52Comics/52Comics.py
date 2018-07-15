#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import os
import sys
import re
import shutil
import random

Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def FindPageUrl(html):
    return re.findall(r'</a></li><li><a href=\'([0-9_]+.html)\'>',html)

def OpenPage(PageList):
    print("打开页面\n");
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    for i in PageList:
        OpenUrl = 'http://www.52kkm.cc/riben/wuyiniao/' + i
        req = urllib.request.Request(OpenUrl,headers = Headers)
        response = urllib.request.urlopen(req)
        response.close()
        html = response.read().decode('gb2312','ignore')
        OpenImgine(html,False)
    return 0

def OpenUrl():
    #http://www.52kkm.org/riben/wuyiniao/*.html
    print("打开Url\n");
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    OpenUrl = 'http://www.52kkm.cc/riben/wuyiniao/5192.html'
    while True:
        try:
            req = urllib.request.Request(OpenUrl)
            response = urllib.request.urlopen(req)
        except urllib.error.URLError:
            return 0
        except UnicodeEncodeError:
            return 0
            
        html = response.read().decode('gb2312','ignore')    #没办法，小网站编码乱搞.
        NextUrl = re.findall(r'下一篇：<a href=\'([0-9\w/_]*.html)\'>',html)
        response.close()
        print("~~~");
        if not NextUrl:
            print('下载完毕\n')
            return 0
        OpenImgine(html,True)
        print(OpenUrl)
        PageList = FindPageUrl(html)
        OpenPage(PageList)
        OpenUrl = 'http://www.52kkm.cc' + NextUrl[0]
    return 0

def OpenImgine(html,mode):
    print("图片下载:\n");
    count = 0
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    if mode:
        DirName = re.findall(r'<h1 class="mhtitle yahei">([\w\S\s_]+)</h1>',html)
        DirName = DirName[0]
        DirName = re.sub(r':',r'：',DirName)
        Path = "D:\\漫画\\%s"% DirName + '\\'
        os.makedirs(Path)
        os.chdir(Path)
    
    ImgineUrl = re.findall('src=\"([\S0-9_\w]+.jpg)',html)
    ImgineUrl = ImgineUrl[0]
    try:
        req = urllib.request.Request(ImgineUrl,headers = Headers)
        response = urllib.request.urlopen(req)
    except urllib.error.URLError:
        return 0

    TmpNameList = ImgineUrl.split('/')
    FileName = TmpNameList[-1]
    with open(FileName, 'wb') as File:
        try:
            File.write(response.read())
        except UnicodeEncodeError:
            return 0
    return 0
    
if __name__ == '__main__':
    print("开始下载:\n");
    OpenUrl()
