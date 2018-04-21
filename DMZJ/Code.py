#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import re
import os
import urllib.request

Origin = 'http://manhua.dmzj.com'
ComicName = ''

def GetTarget():
    Url = input("请输入爬取的DMZJ的漫画页面链接:")
    return Url

def GetCharper(Url,Driver):
    global ComicName
    Driver.get(Url)
    PageHtml = Driver.page_source
    Index = re.findall(r'<li><a title="[\S]+" href="(\S+)" >',PageHtml)
    Dirsname = re.findall(r'<div class="BarTit" id="comicName">(\S+?)</div>',PageHtml)
    ComicName = Path = "D:\\DongmanzhijiaManhua\\" + Dirsname[0]
    if not (os.path.exists(Path)):
        os.makedirs(Path)

    os.chdir(Path)
    
    return Index

def OpenDMZJindex(Url):
    Driver.get(Url)
    PageHtml = Driver.page_source

    return PageHtml

def SavePictures(Index):
    for i in Index:
        Url = Origin + i + '#@page=1'
        print(Url)
        Html = OpenDMZJindex(Url)
        Dirsname = re.findall(r'<title>(\S+?)</title>',Html)
            
        Path = Dirsname[0]
        
        if not (os.path.exists(Path)):
            os.makedirs(Path)

        os.chdir(Path)
            
        UrlPic = re.findall(r'<img name="page[0-9]+" src="//images.dmzj.com/\S+?.jpg">',Html)
        Page = 0
        for each in UrlPic:
            
            NowUrlPic = 'http' + each
            
            FileName = str(Page) + '.jpg'
            with open(FileName,'wb') as F:
                Headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
                Request = urllib.request.Request(Url,None,Heders,method = 'GET')
                Response = urllib.urlopen(Request)
                F.write(Response.read())
                F.close()
                print("第" + str(Page) + "张爬取完成.")

            Page+=1
        os.chdir(ComicName)
        print("单卷下载完成!")
    return 0

if __name__ == '__main__':
    Dcap = dict(DesiredCapabilities.PHANTOMJS)
    Dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36")
    Dcap["phantomjs.page.settings.Accept"] = "*/*"
    Dcap["phantomjs.page.settings.Accept-Encoding"] = "gzip, deflate, sdch, br"
    Dcap["phantomjs.page.settings.Accept-Language"] = "zh-CN,zh;q=0.8"
    Dcap["phantomjs.page.settings.Connection"] = "keep-alive"
    Dcap["phantomjs.page.settings.Host"] = "interface.dmzj.com"
    Dcap["phantomjs.page.settings.Referer"] = "https://manhua.dmzj.com/jiujizhizhuxiazuduichuji/25681.shtml"
    Dcap["phantomjs.page.settings.User-Agent"] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    Driver = webdriver.PhantomJS(desired_capabilities = Dcap)
    
    SavePictures(GetCharper(GetTarget(),Driver))
    Driver.quit()
    Driver.close()


