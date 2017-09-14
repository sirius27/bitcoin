# -*- encoding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
caixin_format = 'http://search.caixin.com/search/search.jsp?keyword={0}&x=0&y=0'
xinhua_format = 'http://so.news.cn/getNews?keyword={0}&curPage=1&sortField=0&searchFields=1&lang=cn'
# remin_
# centerbank_formate =

def request_page(keyword,site='caixin',timeout =10):
    if site == 'caixin':
        page = requests.get(caixin_format.format(keyword),timeout =10)
    elif site == 'xinhua':
        page = requests.get(xinhua_format.format(keyword),timeout =10)
    elif site == 'renmin':
        pass
    return page.text

# def clean_xinhua_title(ke)

def yield_info(keywords, site = 'caixin'):
    if site == 'caixin':
        for keyword in keywords:
            soup = BeautifulSoup(request_page(keyword,'caixin'), 'lxml')
            for item in soup.find_all('div', 'searchxt'):
                url = item.a.get('href')
                title = item.a.string.encode("utf-8")
                time = item.span.encode("utf-8")[7:17]
                time = time +' xx:xx:xx'
                if not any([x in title for x in keywords]):
                    continue
                yield url,title,time

    if site == 'xinhua':
        for keyword in keywords:
            json_str = json.loads(request_page(keyword,'xinhua'))
            if json_str['content']['results']:
                for item in json_str['content']['results']:
                    url = item['url'].encode("utf-8")
                    title = item['title'].encode("utf-8")
                    time = item['pubtime'].encode("utf-8")
                    if not any([x in title for x in keywords]):
                        continue
                    yield url,title,time
