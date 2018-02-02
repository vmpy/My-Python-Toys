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
    #创建文件夹，并将工作目录设置为该文件夹.
    
    FilePath = "D:\\konachan\\"+ PicStyle + '\\'
    if not (os.path.exists(FilePath)):
        os.makedirs(FilePath)
    else:
        Tmp = input('已存在该文件记录,是否继续？请输入[继续\\退出]:\n')
        while Tmp != '继续' and Tmp != '退出':
            Tmp = input("\n指令有误,请重新输入:")

        if Tmp == '退出':
            return 0
    os.chdir(FilePath)
    
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
            print('pass')
            continue
        link = link.group()
        Response = urllib.request.urlopen(link)

        FileName = re.sub(r'%20','&',link.split('/')[-1])

        #如果存在相同的文件就迭代获取下一个.
        if os.path.exists(FileName):
            continue
        
        with open(FileName,'wb') as F:
            F.write(Response.read())
            F.close()
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
    #打开当前文件夹内是否有Page.dat(用于指示爬取到某一页)
    if((os.path.exists('Page.dat'))):
        Tmp = open('Page.dat')
        Page = int(Tmp.read())
        Tmp.close()
    else:
        Page = 1
        
    We = OpenHomeUrl(HomeUrl)
    while(We != 0):
        CopyPic(We)
        Page = Page+1
        HomeUrl = 'https://konachan.com/post?' + 'page=' + str(Page) + '&tags=' + Tags
        
        We = OpenHomeUrl(HomeUrl)
        #写入爬取K站的页面的页数
        with open('Page.dat','wb') as T:
            SomeThing = str(Page)
            T.write(SomeThing)
            T.close()
        
        time.sleep(1)   #防止访问过频，然后GG
