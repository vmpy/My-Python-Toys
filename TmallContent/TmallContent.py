import re
import os
import json
import zlib
import time
import urllib.request

class TmallSpider:
    def __init__(self):
        #保证不重复获取bool self.LastPage
        self.Count = True
        self.Headers = { 'authority':'rate.tmall.com',
                    'method':'GET',
                    'scheme':'https',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'accept-encoding':'gzip, deflate, sdch, br',
                    'accept-language':'zh-CN,zh;q=0.8',
                    'upgrade-insecure-requests':'1',
                    'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

    def GetUrl(self):
        self.Url = input('请输入天猫商品链接:\n')
        self.GetTitle()
        return 0

    def GetTitle(self):
        Headers = self.Headers
        Headers['cache-control'] = 'max-age=0'
        Request = urllib.request.Request(self.Url,None,Headers,method = 'GET')
        Response = urllib.request.urlopen(Request)
        Html = zlib.decompress(Response.read(),16+zlib.MAX_WBITS).decode('GBK')

        self.FileName = re.findall(r'<title>([\s\S]+)</title>',Html)[0]
        return 0
        
    def ExtrackrInformation(self):
        #获取链接中的关键信息:itemId,sellerId
        self.itemId = re.findall(r'id=([0-9]+)',self.Url)[0]
        self.sellerId = re.findall(r'user_id=([0-9]+)',self.Url)[0]
        return 0
    
    def GetContentData(self,Page):
        #Target为临时变量，储存目标链接.
        TargetUrl = 'https://rate.tmall.com/list_detail_rate.htm?itemId=' + self.itemId + '&sellerId=' + self.sellerId + '&currentPage=' + str(Page)
        self.Headers['path'] = '/list_detail_rate.htm?itemId=' + self.itemId + '&sellerId=' + self.sellerId + '&currentPage=' + str(Page)
        
        Request = urllib.request.Request(TargetUrl,None,self.Headers,method = 'GET')
        Response = urllib.request.urlopen(Request)
        Response = zlib.decompress(Response.read(),16+zlib.MAX_WBITS).decode('GBK')
        #获取最后一页.
        if(self.Count):
            self.LastPage = int(re.findall(r'"lastPage":([0-9]+)',Response)[0])
            self.Count = False
        #方括号内才是格式正确的json数据.
        #用字符串切片截取
        beg = Response.find('[')
        end = Response.rfind(']')+1
        if (beg == -1 or end == 0):
            print('\n[!提示]请求获取错误!')
            print('\n[!提示]正在重新获取!')
            return -1
        
        Response = Response[beg:end]
        
        self.JsonData = json.loads(Response)
        
        return self.LastPage

    def WriteFile(self):
        FileName = "D:\\TmallContent\\" + str(self.FileName) + '\\'
        if not (os.path.exists(FileName)):
            os.makedirs(FileName)
        os.chdir(FileName)

        Index = 0
        while(1):
            with open(self.FileName + '.txt','a',encoding = 'utf-8') as File:
                try:
                    File.write("用户:" + self.JsonData[Index]['displayUserNick'] + ':\n')
                    File.write("商品型号:" + self.JsonData[Index]['auctionSku'] + '\n')
                    File.write("评论:" + self.JsonData[Index]['rateContent'] + '\n')
                    File.write("评论日期:" + self.JsonData[Index]['rateDate'] + '\n')
                    File.write("卖家回复:" + self.JsonData[Index]['reply'] + '\n\n')
                    File.close()
                    self.WirtePics(Index)
                    Index += 1
                    
                except IndexError:
                    return 0
        return 0
    
    def WirtePics(self,Index):
        PicIndex = 0
        if not self.JsonData[Index]['pics'][PicIndex]:
                    print('单个用户图片下载完毕')
                    return 0
        FileName = "D:\\TmallContent\\" + str(self.FileName) + '\\' + self.JsonData[Index]['displayUserNick'].replace('*','') + '\\'
        if not (os.path.exists(FileName)):
            os.makedirs(FileName)
        os.chdir(FileName)
        while(1):
            try:
                with open(str(PicIndex) + '.jpg','wb') as File:
                    Response = urllib.request.urlopen('http:' + self.JsonData[Index]['pics'][PicIndex])
                    File.write(Response.read())
                    File.close()
                    PicIndex += 1
            except IndexError:
                #删除因为IndexError跳转于此而JPG是空的,删除文件.
                os.remove(str(PicIndex) + '.jpg')
                os.chdir("D:\\TmallContent\\" + str(self.FileName) + '\\')
                print('单个用户图片下载完毕')
                return 0
        return 0

def IsGoOn(IsFirst):
    if(IsFirst):
        return 1
    
    while(1):
        Tmp = input("\n是否继续?(继续\退出):")
        while Tmp != '继续' and Tmp != '退出':
            Tmp = input("\n指令有误,请重新输入:")

        if Tmp == '继续':
            return 1
        if Tmp == '退出':
            return 0


if __name__ == '__main__':
    IsFirst = True
    while(IsGoOn(IsFirst)):
        IsFirst = False
        Instance = TmallSpider()

        Instance.GetUrl()
        Instance.ExtrackrInformation()
        LastPage = Instance.GetContentData(1)
        Instance.WriteFile()
        print("第1页爬取完毕")
        Page = 2
        while(LastPage >= Page):
            #有时候Response会为空值，原因未知.只好重新尝试.
            if(Instance.GetContentData(Page) == -1):
                continue
            Instance.WriteFile()
            print("第"+str(Page)+"页爬取完毕")
            Page += 1
            time.sleep(3)
