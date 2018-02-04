import re
import os
import zlib
import urllib.request

def GetTarget():
    Tmp = input("请输入要爬取的帖子序号:\n")

    return ('http://bbs.tianya.cn/post-free-' + Tmp)

def OpenUrlAndReturnText(Url):
    
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

def AnalyTextAndWirteFile(Html):
    #创建工作目录
    FilePath = "D:\\TianyaText\\"
    if not (os.path.exists(FilePath)):
        os.makedirs(FilePath)

    os.chdir(FilePath)
    FileName = re.findall(r'<title>(\S+)</title>',Html)[0] + '.txt'

    with open(FileName,'a',encoding = 'utf-8') as File:
        Content = re.findall(r'<div class="atl-con-bd clearfix">[\s\S]+<div class="bbs-content clearfix">([\S\s]+)</div>[\s\S]+<div id="alt_action" class="clearfix">[\s\S]+</div>',Html)[0]
        Content = Content.replace('<br>','\n')
        Content = Content.replace('\t',' ')
        Content = Content.replace(' ','')
        File.write('帖子正文:\n\n'Content)
        File.close()


if __name__ == '__main__':
    Url = GetTarget() + '-1.shtml'
    AnalyTextAndWirteFile(OpenUrlAndReturnText(Url))
