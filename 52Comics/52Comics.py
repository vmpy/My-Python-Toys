#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import os
import sys
import re


def FindPageUrl(html):
    return re.findall(r'</a></li><li><a href=\'([0-9_]+.html)\'>',html)

def OpenPage(PageList):
    
    for i in PageList:
        OpenUrl = 'www.*****.org/*****/*******' + i
        response = urllib.request.urlopen(OpenUrl)
        html = response.read().decode('gb2312','ignore')
        OpenImgine(html,False)
    return 0#返回无用值，不用在意

def OpenUrl():
    #http://www.*****.org/*****/********/*.html
    OpenUrl = 'http://www.*****.org/*****/********/*.html'
    while True:
        try:
            response = urllib.request.urlopen(OpenUrl)
        except urllib.error.URLError as err:
            return 0
            
        html = response.read().decode('gb2312','ignore')	#没办法，小网站编码乱搞.
        NextUrl = re.findall(r'下一篇：<a href=\'([0-9\w/_]*.html)\'>',html)
	if not NextUrl:
		print('下载完毕\n')
		return 0
        OpenImgine(html,True)
        print(OpenUrl)
        PageList = FindPageUrl(html)
        OpenPage(PageList)
        OpenUrl = 'http://www.*****.org' + NextUrl[0]
        response = urllib.request.urlopen(OpenUrl)
    return 0

def OpenImgine(html,mode):
    count = 0
    if mode:
        DirName = re.findall(r'<h1 class="mhtitle yahei">([\w\S\s_]+)</h1>',html)
        DirName = DirName[0]
        DirName = re.sub(r':',r'：',DirName)
        Path = "D:\\漫画\\%s"% DirName + '\\'
        os.makedirs(Path)
        os.chdir(Path)
    
    ImgineUrl = re.findall('src=\"([\S\w]+.jpg)',html)
    ImgineUrl = ImgineUrl[0]
    try:
        response = urllib.request.urlopen(ImgineUrl)
    except urllib.error.URLError as err:
        return 0

    TmpNameList = ImgineUrl.split('/')
    FileName = TmpNameList[-1]
    with open(FileName,'wb') as File:
        File.write(response.read())
        File.close()
    return 0
    
if __name__ == '__main__':
	OpenUrl()
  
