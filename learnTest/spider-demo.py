from urllib import request
import ssl
import re
# req_csdn = request.Request('https://blog.csdn.net/meteor_93')
# req_csdn.add_header('User-Agent',
#                     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
# html_csdn = request.urlopen(req_csdn).read().decode('utf-8')
# print(html_csdn)


# 获取html内容
def getHtml(url):
    page = request.urlopen(url)
    html = page.read()
    html = html.decode('utf-8')
    return html

# 获取title
def get_title(html):
    reg = r'<title>(.*)</title>'
    content_title = re.compile(reg)
    result = re.findall(content_title, html)
    return result

# 创建ssl证书
ssl._create_default_https_context = ssl._create_unverified_context
url = "https://blog.csdn.net/meteor_93"
html = getHtml(url)
title = get_title(html)
print(title)