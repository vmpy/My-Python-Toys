#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import time
import urllib.request

#https://konachan.com/post?tags=data

def GetPicStyleName():
    PicStyle = str(input("请输入要在K站爬取图片的类型：\n"))
    #HomeUrl = "https://konachan.com/post?tags=" + PicStyle
    return PicStyle

def OpenHomeUrl(Url):
    Headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    Req = urllib.request.Request(Url,None,Headers,method = 'GET')

    Response = urllib.request.urlopen(Req)
    Html = Response.read().decode('UTF-8','ignore')
    if re.search(r'Nobody here but us chickens!',Html) != None:
        return 0
    PicUrlResult = re.findall(r'<span class="plid">#pl (https://konachan.com/post/show/[0-9]+)</span>',Html)

    return PicUrlResult

def CopyPic(PicResult):
    count = 0
    for i in PicResult:
        
        Headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        Req = urllib.request.Request(i,None,Headers,method = 'GET')

        Response = urllib.request.urlopen(Req)
        Html = Response.read().decode('UTF-8','ignore')
        
        link = re.search(r'https://konachan.com/sample/[\S]+/Konachan.com[\S]+sample.jpg',Html)

        #如果其不存在类似链接,迭代获取下一个
        if not link:
            continue
        link = link.group()
        Response = urllib.request.urlopen(link)

        FileName = re.sub(r'%20','&',link.split('/')[-1])

        #如果存在相同的文件就迭代获取下一个.
        if os.path.exists(FileName):
            continue
        
        with open(FileName,'wb') as File:
            File.write(Response.read())
            File.close()
            count = count+1
        print("第" + str(count) + "张"+"下载完成!")
        
    return 0


if __name__ == '__main__':
    
    Path = "D:\\konachan\\"
    if not (os.path.exists(Path)):
        os.makedirs(Path)
    os.chdir(Path)
    Tags = GetPicStyleName()
    HomeUrl = "https://konachan.com/post?tags=" + Tags
    
    Page = 1
    We = OpenHomeUrl(HomeUrl)
    while(We != 0):
        CopyPic(We)
        Page = Page+1
        HomeUrl = 'https://konachan.com/post?' + 'page=' + str(Page) + '&tags=' + Tags
        We = OpenHomeUrl(HomeUrl)
        time.sleep(5)   #防止访问过频，然后GG
