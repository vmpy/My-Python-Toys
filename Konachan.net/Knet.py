#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import time
import zlib
import urllib.request

#https://konachan.com/post?tags=data

Tag = str()

def GetPicStyleName():
    """
    获取K站内罗马音Tags.
    Returns:PicStyle:罗马音Tag.
    """
    global Tag
    Tag = PicStyle = str(input("请输入要在K站爬取图片的类型：\n"))
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
    """
    获取Tag相关图片浏览页面.
    Args:
        Url:页面链接.
    Returns:
        1.所有页面爬取完毕，返回0.
        2.PicUrlResult:返回一个关于所有图片详细页面的地址.
    """
    Headers = {'authority':'konachan.com',
                'method':'GET',
                'path':'/post?tags='+Tag,
                'scheme':'https',
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding':'gzip, deflate, sdch, br',
                'accept-language':'zh-CN,zh;q=0.8',
                'cache-control':'max-age=0',
                'referer':'https://konachan.com/',
                'upgrade-insecure-requests':'1',
                'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    Req = urllib.request.Request(Url,None,Headers,method = 'GET')

    Response = urllib.request.urlopen(Req)
    Html = zlib.decompress(Response.read(),16+zlib.MAX_WBITS).decode('utf-8')
    if re.search(r'Nobody here but us chickens!',Html):
        return 0
    PicUrlResult = re.findall(r'<span class="plid">#pl (https://konachan.com/post/show/[0-9]+)</span>',Html)

    return PicUrlResult

def CopyPic(PicResult):
    """
    找到图片链接，写入文件.
    Returns:None
    """
    count = 0
    for i in PicResult:
        
        Headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                 'authority':'konachan.com',
                 'method':'GET',
                 'scheme':'https',
                 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                 'accept-encoding':'gzip, deflate, sdch, br',
                 'accept-language':'zh-CN,zh;q=0.8',
                 'cache-control':'max-age=0'}
        
        Req = urllib.request.Request(i,None,Headers,method = 'GET')

        Response = urllib.request.urlopen(Req)
        Html = zlib.decompress(Response.read(),16+zlib.MAX_WBITS).decode('utf-8')
        try:
            link = re.findall(r'(https://konachan.com/sample/[a-z0-9A-Z]+/Konachan.com[\S]+sample.jpg)',Html)[0]

        #如果其不存在类似链接,是因为源代码使用Js嵌入图片
        except IndexError:
            link = re.findall(r'(https:\\/\\/konachan.com\\/image\\/[a-z0-9]+\\/Konachan.com[\S]+.jpg)',Html)
            #re贪婪模式会获取许多个相似链接，只取第一个.
            end = link[0].find('"')
            link = link[0][0:end]
        
        link = link.replace('\\','')
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
        
    return None


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
            SomeThing = (str(Page)).encode('utf-8')
            T.write(SomeThing)
            T.close()
        print('第' + str(Page) + '页下载完成!')
        time.sleep(1)   #防止访问过频，然后GG
