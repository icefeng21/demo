import os

import requests as requests
from lxml import etree

# s = requests.Session()
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5666.197 Safari/537.36',
# }
# r = s.get('https://youku.com', headers=headers, timeout=3)
# r.encoding = 'utf-8'
# print(r.cookies.items())
#
# r = s.get('https://youku.com', headers=headers)
# r.encoding = 'utf-8'
# print(r.cookies.items())

proxyUser = "HY588KO97XC8RH1D"
proxyPass = "189BDBC4FCBF6184"

proxies = {
    'http': f'http://{proxyUser}:{proxyPass}@http-dyn.abuyun.com:9020',
    'https': f'http://{proxyUser}:{proxyPass}@http-dyn.abuyun.com:9020'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5666.197 Safari/537.36',
}

for i in range(0, 1):
    try:
        r = requests.get('https://www.baidu.com', proxies=proxies, headers=headers)

        # if os.path.exists('./file/ip.html'):
        #     os.remove('./file/ip.html')
        #
        # with open('./file/ip.html', 'w+', encoding='utf-8') as f:
        #     f.write(r.text)

        data = etree.HTML(r.text)
        print(data)
        # data = etree.parse('./file/ip.html', etree.HTMLParser())
        # ip_info = data.xpath('//*[@id="main_form"]/p[0]/text()')
        element_list = data.xpath('//*')
        for element in element_list:
            print(element)

        # print(ip_info)
    except Exception as e:
        print(f' error is :{str(e)}')
        pass


# //*[@id="main_form"]/p[1]
#//*[@id="main_form"]/p[1]
# //*[@id="main_form"]/p[2]/input
#
# //*[@id="main_form"]/p[2]/input
