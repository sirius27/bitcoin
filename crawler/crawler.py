#-*-coding:utf-8-*-
import urllib
import re
import time
import json
import Queue
import send_email

queue_size = 5
'''
class NewsQueue():
    def __init__(self, queue_name, queue_size=queue_size):
        self.name = queue_name
        self.size = queue_size
        self.queue = Queue.Queue(0)

    def push(self, news):
        self.queue.put(news)
        if self.queue.qsize() > self.size:
            self.queue.get()
        return True

    def empty(self):
        self.queue.empty

    def to_list(self):
        return list(self.queue.queue)
'''

def people_finance():
    source = 'http://finance.people.com.cn/'
    data = urllib.urlopen(source)
    txt = data.read()
    year = time.strftime("%Y",time.localtime())
    date = time.strftime("%m%d",time.localtime())

    url_reg_exp = '''href='(/n1/'''+year+'/'+date+'/c'+'.+?'+'''\.html)' target="_blank">(.+?)</a>'''
    articles_info = re.findall(url_reg_exp,txt)
    article_urls = ['http://finance.people.com.cn' + article_info[0] for article_info in articles_info]
    article_titles = [article_info[1] for article_info in articles_info]
    print article_urls[0].decode('gbk')
    print article_titles[0].decode('gbk')
    return {url:title for url,title in zip(article_urls[:queue_size], article_titles[:queue_size])}

def ok():
    source = 'https://www.okcoin.cn/service.html'
    data = urllib.urlopen(source)
    txt = data.read()
    year = time.strftime("%Y",time.localtime())
    date = time.strftime("%m%d",time.localtime())

    reg_exp = 'https:&#47;&#47;www.okcoin.cn&#47;t-([0-9].+?).html"\s'+'''title="(.+?)"'''
    #re.findall('title="(.+)"',a)[0].decode('utf-8')
    articles_info = re.findall(reg_exp,txt)
    article_urls = ['http://www.okcoin.cn/t-' + article_info[0] + '.html' for article_info in articles_info]
    article_titles = [article_info[1] for article_info in articles_info]

    return {url:title for url,title in zip(article_urls[:queue_size], article_titles[:queue_size])}

def get_news():
    news_dict = dict()
    news_dict['people'] = people_finance()
    news_dict['ok'] = ok()
    return news_dict

def update(cache_dict, news_dict):
    change = False
    for k,v in news_dict.items():
        if not cache_dict[k] == v:
            change = True
            cache_dict[k] = v
    return change

def generate_content(cache_dict):
    s = ''
    for k,v in cache_dict.items():
        s += k+':\n'
        for url, title in v.items():
            s += url
            s += '\n'
            s += title
            s += '\n'
        s += '\n'
    return s
    
def main():
    news_dict = get_news()
    change = update(cache_dict, news_dict)
    content = generate_content(cache_dict)
    if change:
        for receiver in receiver_lst:
            send_email.send_email(receiver, content)

if __name__ == '__main__':
    cache_dict = {'people':dict(), 'ok':dict()}
    receiver_lst = ['colin.qian@meritco-group.com', 'duanwei_93@163.com']   
    receiver_lst = ['duanwei_93@163.com']
    '''
    while True:
        time.sleep(5)
        try:
            main()
            #continue
        except KeyboardInterrupt:
            with open('data.json', 'w') as f:
                json.dump(cache_dict, f)
            exit()
        except:
            print 'unexpected error'
            continue
            '''
    main()
