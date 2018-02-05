import re
import os
import json
import zlib
import time
import urllib.request

class TmallSpider:
    def __init__(self):
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
        return 0
    
    def ExtrackrInformation(self):
        self.itemId = re.findall(r'id=([0-9]+)',self.Url)[0]
        self.sellerId = re.findall(r'user_id=([0-9]+)',self.Url)[0]
        return 0
    
    def GetContentData(self,Page):
        TargetUrl = 'https://rate.tmall.com/list_detail_rate.htm?itemId=' + self.itemId + '&sellerId=' + self.sellerId + '&currentPage=' + str(Page)
        self.Headers['path'] = '/list_detail_rate.htm?itemId=' + self.itemId + '&sellerId=' + self.sellerId + '&currentPage=' + str(Page)
        
        Request = urllib.request.Request(TargetUrl,None,self.Headers,method = 'GET')
        Response = urllib.request.urlopen(Request)
        Response = zlib.decompress(Response.read(),16+zlib.MAX_WBITS).decode('GBK')
        #获取最后一页.
        self.LastPage = int(re.findall(r'"lastPage":([0-9]+)',Response)[0])
        #方括号内才是格式正确的json数据.
        Response = re.findall(r'"rateList":(\[[\S\s]+\]),"searchinfo":"","tags":""}',Response)[0]
        self.JsonData = json.loads(Response)
        return self.LastPage

    def WriteFile(self):
        FileName = "D:\\TmallContent\\" + str(self.itemId) + '\\'
        if not (os.path.exists(FileName)):
            os.makedirs(FileName)
        os.chdir(FileName)

        Index = 0
        with open('商品序号：' + str(self.itemId) + '.txt','a',encoding = 'utf-8') as File:
            try:
                File.write("用户:" + self.JsonData[Index]['displayUserNick'] + ':\n')
                File.write("商品型号:" + self.JsonData[Index]['auctionSku'] + '\n')
                File.write("评论:" + self.JsonData[Index]['rateContent'] + '\n')
                File.write("评论日期:" + self.JsonData[Index]['rateDate'] + '\n')
                File.write("卖家回复:" + self.JsonData[Index]['reply'] + '\n\n')
                File.close()
                Index += 1
            except IndexError:
                return 0 

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
    while(IsGoOn()):
        Instance = TmallSpider()

        Instance.GetUrl()
        Instance.ExtrackrInformation()
        LastPage = Instance.GetContentData(1)
        Instance.WriteFile()
        print("第1页爬取完毕")
        Page = 2
        while(LastPage >= Page):
            Instance.GetContentData(Page)
            Instance.WriteFile()
            print("第"+str(Page)+"页爬取完毕")
            Page += 1
            time.sleep(3)