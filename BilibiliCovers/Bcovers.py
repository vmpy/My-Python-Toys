#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import zlib
import urllib.request

HomeUrl = 'https://www.bilibili.com/video/av'
ImagineName = 'None'

def GetTarget():
    Num = input("请输入Bilibili视频Av号(请输入纯数字):\n")
    while re.match(r'[^(avAV0-9)]+',Num):       #如果输入为非纯数字字符串
        Num = input("输入有误,请重新输入Bilibili视频Av号(请输入正确编码):\n")
    #当不同人喜欢在数字前加上'AV':
    while(re.match(r'[AaVv]+',Num)):
        if 'a' in Num and 'v' in Num and Num[:2] == 'av':
            Num = Num[2:]
            break
        elif 'A' in Num and 'V' in Num and Num[:2] == 'AV':
            Num = Num[2:]
            break
        elif 'A' in Num and 'v' in Num and Num[:2] == 'Av':
            Num = Num[2:]
            break
        else:
            Num = input("输入有误,请重新输入Bilibili视频Av号(请输入正确编码):\n")
    return Num

def OpenUrl(Num):
    global ImagineName
    ImagineName = 'Av' + Num
    
    Url = HomeUrl + Num     #B站视频网站构成
    Headers ={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch, br',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Connection':'keep-alive',
                'Host':'www.bilibili.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    Req = urllib.request.Request(Url,None,Headers,method = 'GET')

    Response = urllib.request.urlopen(Req)
    Html = Response.read()
    Html = zlib.decompress(Html,16+zlib.MAX_WBITS).decode('utf-8','ignore')      #bilibili采用gzip压缩网页源码,zlib.decompress解压缩.
    return Html

def SaveImagine(Html):
    ImagineUrl = re.findall(r'<img src="(//i[0-9].hdslb.com/bfs/archive/\S+.[a-z]+)" style="display:none;" class="cover_image"/>',Html)
    ImagineUrl = 'http:' + ImagineUrl[0]
    Path = "D:\\BilibiliCovers\\"           #单独创建文件夹
    if not (os.path.exists(Path)):
        os.makedirs(Path)
    os.chdir(Path)

    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    Req = urllib.request.Request(ImagineUrl,None,Headers,method = 'GET')
    Response = urllib.request.urlopen(Req)
    FileName = ImagineName +' 封面'+ '.jpg'         #av号+图片后缀，组合为文件名称
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
