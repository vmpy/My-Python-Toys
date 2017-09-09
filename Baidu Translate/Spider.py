# -*- coding: <utf-8> -*-
import urllib.request
import urllib.parse
import re


url = 'http://fanyi.baidu.com/v2transapi'
while True:
        while True:
                choice = str(input("请输入转换模式:(English-中文:EN)(中文-English:ZH)(退出程序:Q!)"))
                if choice == 'EN':
                        break;
                elif choice == 'ZH':
                        break;
                elif choice == 'Q!':
                        quit();
                

        while True:
                
            enter = str(input("请输入你要翻译的词句:（输入N!退出）"))
            data = dict()
            if enter != 'N!':
                head = dict()
                head['User-Agent'] = 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
                if choice == 'EN':
                        data['from'] = 'en'
                        data['to'] = 'zh'
                else:
                        data['from'] = 'zh'
                        data['to'] = 'en'
                data['query'] = enter
                data['transtype'] = 'translang'
                data['simple_means_flag'] = '3'

                data = urllib.parse.urlencode(data).encode('utf-8')
                example = urllib.request.Request(url,data,head)
                response = urllib.request.urlopen(example)

                html = response.read().decode('unicode_escape')
                if choice == 'ZH':
                        result = re.search(r'\"dst\":\"[\w\s0-9\+\-\*/\',\.\{\}\[\]\~\(\)\^\|=\&%\$#!]+\"',html)
                        if result == None:
                                break;
                        answer = result.group()
                else:
                        result = re.search(r'\"dst\":\"[\S\s0-9\{\}\[\]\+\-\*\~\(\)\^\|=\&%\$#!/,]+\",',html)
                        if result == None:
                                break;
                        answer = result.group()
                        index = answer.find(',')
                if choice == 'EN' and result:
                        print("你所输入百度翻译结果为:" + answer[6:index])
                elif choice == 'ZH' and result:
                        print("你所输入百度翻译结果为:" + answer[6:])
            else:
                break;
