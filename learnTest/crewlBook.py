# encoding: utf-8


import requests, os, time
from lxml import etree
from loguru import logger
import random


class NovelCrawler:
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    ]
    headers = {
        'User-Agent': random.choice(user_agent_list)
    }

    def crawl_chapter_list(self, url):
        response = requests.get(url, headers=self.headers)
        # 使用etree进行解析
        data = etree.HTML(response.text)
        book_name = data.xpath('//div[@class = "jj960"]/h1[1]/text()')[0]
        chapter_list = data.xpath('//td[@align = "center"]//td[@align = "left"]//a/@href')
        return book_name, chapter_list
        pass

    def crawl_chapter_content(self, url, count):
        response = ''
        try:
            response = requests.get(url, headers=self.headers, timeout=0.8)
        except:
            logger.info(f'请求超时, url = {url}')
            # 手动重试
            if count <= 3:
                return self.crawl_chapter_content(url, count + 1)
            else:
                return '', ''
        if response is None:
            return '', ''

        try:
            # 使用etree进行解析
            data = etree.HTML(response.text)
        except:
            logger.info(f'解析响应出错, response = {response}, url = {url}')
            return "", ""

        chapter_name = data.xpath('//div[@id = "maincontent"]/h2/text()')[0]
        chapter_content = ''
        try:
            chapter_content = data.xpath('//div[@id = "content"]/p/text()')[0] + '\n'
        except:
            print(url)
            print(data.xpath('//div[@id = "content"]/p/text()'))
            pass
        div_list = data.xpath('//div[@id = "content"]/div')
        for div in div_list[:-2]:
            line = ''.join(div.xpath('.//text()'))
            chapter_content += line + '\n'
        return chapter_name, chapter_content
        pass

    def crawl_book(self, url):
        book_name, chapter_list = self.crawl_chapter_list(url)

        content_list = []
        for i, chapter in enumerate(chapter_list):
            logger.info(f'正在获取第{i}章')
            chapter_name, chapter_content = self.crawl_chapter_content(chapter, count=1)
            content_list.append(chapter_name)
            content_list.append(chapter_content)
            time.sleep(0.8)

        # 写入文件
        path = './file/'
        if os.path.exists(path) is False:
            os.mkdir(path)
        file_name = path + book_name + '.txt'
        if os.path.exists(file_name):
            os.remove(file_name)

        content = '\n'.join(str(i) for i in content_list)
        with open(path + book_name + '.txt', 'w+', encoding='utf-8') as f:
            f.write(content)
        pass


if __name__ == '__main__':
    cralwer = NovelCrawler()
    url = 'http://guoxue.lishichunqiu.com/shibu/zizhitongjian/'
    cralwer.crawl_book(url)
    pass