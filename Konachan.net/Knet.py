#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib.request
import os

#原始地址
#https://konachan.com/post?tags=data

def GetPicStyleName():
    PicStyle = str(input("请输入要在K站爬取图片的类型：\n"))
    return PicStyle

def OpenHomeUrl(Url):
    Headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    Req = urllib.request.Request(Url,None,Headers,method = 'GET')

    Response = urllib.request.urlopen(Req)
    Html = Response.read().decode('UTF-8','ignore')
    #如果搜索未出现结果就结束.
    if re.search(r'Nobody here but us chickens!',Html) != None:
        print('Nobody here but us chickens!')
        return 0
    PicUrlResult = re.findall(r'<span class="plid">#pl (https://konachan.com/post/show/[0-9]+)</span>',Html)

    return PicUrlResult

def CopyPic(PicResult):
    for i in PicResult:
        #分别打开每一个图片页面
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
        
        #将链接中的'%20'替换为'&'.
        FileName = re.sub(r'%20','&',link.split('/')[-1])
        
        with open(FileName,'wb') as F:
            F.write(Response.read())
            F.close()
        print("下载完成!")
    return 0


if __name__ == '__main__':
    #创建一个文件夹:
    Path = "D:\\konachan\\"
    #如果D盘不存在此文件夹，就创建.
    if not (os.path.exists(Path)):
        os.makedirs(Path)
        
    #进入该文件夹
    os.chdir(Path)
    #图片风格关键字获取.
    Tags = GetPicStyleName()
    HomeUrl = "https://konachan.com/post?tags=" + Tags
    
    Page = 1
    We = OpenHomeUrl(HomeUrl)
    while(We != 0):
        CopyPic(We)
        We = OpenHomeUrl(HomeUrl)
        Page = Page+1
        HomeUrl = 'https://konachan.com/post?' + 'page=' + str(Page) + '&tags=' + Tags
