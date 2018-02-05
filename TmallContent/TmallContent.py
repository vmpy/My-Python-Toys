import re
import json
import zlib
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
        #https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.175488665jKz7d&id=35685793847&skuId=3668976687307&user_id=1713424658&cat_id=2&is_b=1&rn=3a6f4b745891b9b2e6bbd62c62aa6b13
        #https://rate.tmall.com/list_detail_rate.htm?itemId=35685793847&sellerId=1713424658&currentPage=1&append=0&content=1
    def ExtrackrInformation(self):
        self.itemId = re.findall(r'id=([0-9]+)',self.Url)[0]
        self.sellerId = re.findall(r'user_id=([0-9]+)',self.Url)[0]

    def GetContentData(self,Page):
        TargetUrl = 'https://rate.tmall.com/list_detail_rate.htm?itemId=' + self.itemId + '&sellerId=' + self.sellerId + '&currentPage=' + str(Page)
        self.Headers['path'] = '/list_detail_rate.htm?itemId=' + self.itemId + '&sellerId=' + self.sellerId + '&currentPage=' + str(Page)
        
        Request = urllib.request.Request(TargetUrl,None,self.Headers,method = 'GET')
        Response = urllib.request.urlopen(Request)
        Response = zlib.decompress(Response.read(),16+zlib.MAX_WBITS).decode('GBK')

        #获取最后一页.
        self.LastPage = re.findall(r'"lastPage":([0-9]+)',Response)
        #方括号内才是格式正确的json数据.
        Response = re.findall(r'"rateList":(\[[\S\s]+\]),"searchinfo":"","tags":""}',Response)[0]
        JsonData = json.loads(Response)



if __name__ == '__main__':
    Instance = TmallSpider()

    Instance.GetUrl()
    Instance.ExtrackrInformation()
    Instance.GetContentData(1)
