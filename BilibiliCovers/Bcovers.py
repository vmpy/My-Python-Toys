#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import urllib.request

#利用B站中搜索AV号时出现的结果的封面，进行下载.
HomeUrl = 'https://search.bilibili.com/all?keyword='

def GetTarget():
    Num = input("请输入Bilibili视频Av号(请输入纯数字):\n")
    while re.match(r'[^(0-9)]+',Num):       #如果输入为非纯数字字符串
        Num = input("输入有误,请重新输入Bilibili视频Av号(请输入纯数字):\n")
    return Num

def OpenUrl(Num):
    Url = HomeUrl + Num
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    Req = urllib.request.Request(Url,None,Headers,method = 'GET')

    Response = urllib.request.urlopen(Req)

    Html = Response.read().decode('utf-8','ignore')
    return Html

def SaveImagine(Html):
    ImagineUrl = re.findall(r'data-src=\"(//i1.hdslb.com/bfs/archive/\S+.jpg)\"',Html)
    ImagineUrl = 'http:' + ImagineUrl[0]
    Path = "D:\\BilibiliCovers\\"           #单独创建文件夹
    if not (os.path.exists(Path)):
        os.makedirs(Path)
    os.chdir(Path)

    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    Req = urllib.request.Request(ImagineUrl,None,Headers,method = 'GET')
    Response = urllib.request.urlopen(Req)

    ImagineName = re.findall(r'<span class="avid type">([a-z0-9]+)</span>',Html)        #re.findall返回一个tuple
    FileName = ImagineName[0] + '.jpg'          #av号+图片后缀，组合为文件名称
    with open(FileName,'wb') as File:
        File.write(Response.read())
        File.close()
        print("封面下载完成!")
    
if __name__ == '__main__':
    while(1):
        SaveImagine(OpenUrl(GetTarget()))
        Tmp = input("\n是否继续?(继续\退出):")
        while Tmp != '继续' and Tmp != '退出':
            Tmp = input("\n请重新输入:")

        if Tmp == '继续':
            continue
        if Tmp == '退出':
            break
