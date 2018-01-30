
import urllib.request
import urllib.parse
import json
import zlib

UrlAPI = 'http://fanyi.baidu.com/v2transapi'

Headers = {'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Content-Length':'135',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'fanyi.baidu.com',
        'Origin':'http://fanyi.baidu.com',
        'Referer':'http://fanyi.baidu.com/?aldtype=16047',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'}

def MakeChoice():
        Tmp = int(input('请输入翻译方式:\n1.中文-英文\n2.英文-中文\n\n'))
        while(Tmp != 1 and Tmp != 2):
                Tmp = int(input('请重新输入翻译方式:\n1.中文-英文\n2.英文-中文\n\n'))

        return Tmp

def MakeData(Way):
        if(Way == 1):
                data = {'from':'zh',
                'to':'en',
                'transtype':'translang',
                'simple_means_flag':'3',
                'sign':'375435.88506',
                'token':'a67933e6193cd61cf3d18cd39bb9b10e'}
        else:
                data = {'from':'en',
                'to':'zh',
                'transtype':'translang',
                'simple_means_flag':'3',
                'sign':'375435.88506',
                'token':'a67933e6193cd61cf3d18cd39bb9b10e'}

        query = input('请输入要翻译的原文:\n')
        data['query'] = query

        data = urllib.parse.urlencode(data).encode('utf-8')

        return data

def GetJsonData(data):
        Request = urllib.request.Request(UrlAPI,data,Headers,method = 'POST')
        Response = urllib.request.urlopen(Request)
        JsonData = zlib.decompress(Response.read(),16+zlib.MAX_WBITS).decode('utf-8')
        JsonData = json.loads(JsonData)
        return JsonData

def GetResult(JsonData):
        print('翻译结果为:' + str(JsonData['trans_result']['data'][0]['dst']))

if __name__ == '__main__':
        GetResult(GetJsonData(MakeData(MakeChoice())))
        
