#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import zlib
import time
import re
import urllib.request

def GetVideoNumber():
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

def GetCommentData(Num):  
    #是否已经爬取过热评
    IsSaveHots = False

    #创建文件夹，并将工作目录设置为该文件夹.
    FilePath = "D:\\BilibiliComment\\" + 'Av' + str(Num) + '\\'
    if not (os.path.exists(FilePath)):
        os.makedirs(FilePath)
    else:
        Tmp = input('已存在该文件记录,是否继续？请输入[继续\\退出]:\n')
        while Tmp != '继续' and Tmp != '退出':
            Tmp = input("\n指令有误,请重新输入:")

        if Tmp == '退出':
            return 0
    os.chdir(FilePath)
    #评论API
    Url = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn='
    Page = 1
    Headers = { 'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate, sdch, br',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Connection':'keep-alive',
                'Host':'api.bilibili.com',
                'Referer':'https://www.bilibili.com/video/av14650141/',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    while(1):
        Url = Url + str(Page) + '&type=1&oid=' + Num + '&sort=0'
        Request = urllib.request.Request(Url,None,Headers,method = 'GET')
        Response = urllib.request.urlopen(Request)
        JsonData = zlib.decompress(Response.read(),16+zlib.MAX_WBITS).decode('utf-8')

        Comment = json.loads(JsonData)
        
        #热评爬取部分:
        if(IsSaveHots == False):
            SaveHots(Comment)
            IsSaveHots = True

        if(SaveNormalReplies(Comment,Page)):
            return 0
        Page += 1
        #重置Url的值
        Url = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn='
        time.sleep(1)       #防止访问过频，然后GG
    return 0

def SaveHots(Comment):
    #json数据的索引
    Index = 0
    while(1):
        try:
            FileName = '评论区热评.txt'
            with open(FileName,'a',encoding = 'utf-8') as F:
                F.write(Comment['data']['hots'][Index]['member']['uname'])
                F.write(':\n')
                F.write(Comment['data']['hots'][Index]['content']['message'])
                F.write('\n\n')
                F.close()
                Index+=1
        except IndexError:
            print('热评爬取完毕!')
            return 0

def SaveNormalReplies(Comment,Page):
    #json数据的索引
    Index = 0
    while(1):
        try:
            FileName = '评论区评论.txt'
            #Python的编码真是一个大坑……
            with open(FileName,'a',encoding='utf-8') as F:
                F.write('第' + str(Comment['data']['replies'][Index]['floor']) + '楼:\n')
                F.write(Comment['data']['replies'][Index]['member']['uname'])
                F.write(':\n')
                F.write(Comment['data']['replies'][Index]['content']['message'])
                F.write('\n')
                F.close()
                SaveNormalRepliesReplies(Comment,Index)
                with open(FileName,'a',encoding='utf-8') as E:
                    E.write('\n')
                    E.close()
                
                if(Comment['data']['replies'][Index]['floor'] == 1):
                    print('第'+ str(Page) + '页' + '评论区评论爬取完毕!')
                    with open(FileName,'a',encoding='utf-8') as T:
                        T.write('爬取时间:' + (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                        T.close()
                    print('所有评论爬取完毕\n')
                    return 1
                Index+=1
        #当Index超出字典索引范围时，说明爬取完毕.
        except IndexError:
            print('第'+ str(Page) + '页' + '评论区评论爬取完毕!')
            return 0

#爬取评论楼中楼.
def SaveNormalRepliesReplies(Comment,Index):
    #json数据的索引
    IndexOfFloor = 0
    while(1):
        try:
            FileName = '评论区评论.txt'
            #Python的编码真是一个大坑……
            with open(FileName,'a',encoding='utf-8') as F:
                F.write('\t回复:' + Comment['data']['replies'][Index]['replies'][IndexOfFloor]['member']['uname'])
                F.write(':' + Comment['data']['replies'][Index]['replies'][IndexOfFloor]['content']['message'] + '\n')
                F.close()
                IndexOfFloor+=1
                
        #当IndexOfFloor超出字典索引范围时，说明楼中楼爬取完毕.
        except IndexError:
            with open(FileName,'a',encoding='utf-8') as Fe:
                Fe.write('\n')
                Fe.close()
            return 0

def IsGoOn():
    while(1):
        Tmp = input("\n是否继续?(继续\退出):")
        while Tmp != '继续' and Tmp != '退出':
            Tmp = input("\n指令有误,请重新输入:")

        if Tmp == '继续':
            return 1
        if Tmp == '退出':
            return 0
    
if __name__ == '__main__':
    GetCommentData(GetVideoNumber())
    while(IsGoOn()):
        GetCommentData(GetVideoNumber())
