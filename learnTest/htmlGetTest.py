import requests
from lxml import etree

content = input("请输入内容：")
# step_1:指定url
url = 'http://www.syiban.com/search/index/init.html?modelid=1&q=' + content
# step_2:发起请求
# get方法会返回一个响应对象
response = requests.get(url=url)
# step_3:获取响应数据.text返回的是字符串形式的响应数据
page_text = response.text
tree = etree.HTML(page_text)
question = tree.xpath('//span[@class="title_color"]')
answer = tree.xpath('//div[@class="yzm-news-right"]/p/span')
print(question)
for index, value in enumerate(question):
    print(question[index].xpath('string()'))
    print(answer[index].xpath('string()'))
# step_4:持久化存储
with open('./强国.html', 'w', encoding='utf-8') as fp:
    fp.write(page_text)
print('爬取数据结束！！！')
