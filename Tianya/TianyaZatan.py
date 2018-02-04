import re
import os
import zlib
import urllib.request

MaxPage = int() #获取最大页数的全局变量.
FileNameAll = str() #全局变量文件名字.

def GetTarget():
    Tmp = input("请输入要爬取的帖子序号:\n")
    return ('http://bbs.tianya.cn/post-free-' + Tmp)

def OpenUrlAndReturnText(Url):
    #喜闻乐见的Headers
    Headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Host':'bbs.tianya.cn',
                'Referer':'http://bbs.tianya.cn/post-free-1063397-1.shtml',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

    Request = urllib.request.Request(Url,None,Headers,method = 'GET')
    Response = urllib.request.urlopen(Request)
    
    Html = Response.read().decode('utf-8')

    return Html

def AnalyTextAndWirteFile(Html,N):
    global MaxPage
    global FileNameAll
    #创建工作目录
    FilePath = "D:\\TianyaText\\"
    if not (os.path.exists(FilePath)):
        os.makedirs(FilePath)

    os.chdir(FilePath)
    if N:
        FileNameAll = FileName = re.findall(r'<title>(\S+)</title>',Html)[0] + '.txt'

        with open(FileName,'a',encoding = 'utf-8') as File:
            Content = re.findall(r'<div class="atl-con-bd clearfix">[\s\S]+<div class="bbs-content clearfix">([\S\s]+)</div>[\s\S]+<div id="alt_action" class="clearfix">[\s\S]+</div>',Html)[0]
            Content = Content.replace('<br>','\n')
            Content = Content.replace('\t',' ')
            Content = Content.replace(' ','')
            Content = Content.replace('　','')
            File.write('帖子正文:\n\n' + Content + '\n帖子回复:\n')
            File.close()
        MaxPage = int(re.findall(r'…\s<a href="/post-free-[0-9\-]+.shtml">(\S+?)</a>',Html)[0])
    
    #用正则找到所有关于帖子回复的源码内容:
    #我终于认识到了?非贪婪限定符的重要性:
    RepliesUser = re.findall(r'js_username="(\S+)"',Html)   #回复用户列表
    RepliesUserTime = re.findall(r'js_resTime="([0-9\-]+ [0-9:]+)">',Html)  #回复用户时间列表
    RepliesContent = re.findall(r'<div class="bbs-content">([\s\S]+?)</div>',Html)  #回复内容列表

    Index = 0
    with open(FileNameAll,'a',encoding = 'utf-8') as File:
        while(Index < len(RepliesUser)):
            File.write("第"+str(Index + 1)+"楼:\n")
            File.write(RepliesUser[Index] + ':\n')
            File.write(RepliesUserTime[Index] + '\n')
            File.write(RepliesContent[Index].replace(' ','').replace('\t',' ').replace('<br>','\n').replace('　',''))
            File.write('\n')
            Index += 1

        File.close()

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
    while(IsGoOn())
        HomeUrl = GetTarget()
        Url = HomeUrl + '-1.shtml'
        AnalyTextAndWirteFile(OpenUrlAndReturnText(Url),True)
        print('第1页爬取完毕')


        Page = 2
        while(Page <= MaxPage):
            Url = HomeUrl + '-' + str(Page) + '.shtml'
            AnalyTextAndWirteFile(OpenUrlAndReturnText(Url),False)
            print('第' + str(Page) + '页爬取完毕')
            Page += 1

        print('全帖爬取完毕')
    #删除俩全局变量.
    del MaxPage
    del FileNameAll
