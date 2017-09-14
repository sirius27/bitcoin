# -*- encoding:utf-8 -*-

import requests
import os
from bs4 import BeautifulSoup
import arrow as ar
import re

from send_email import *
from site_analyze import *

date = ar.now().strftime(format='%Y-%m-%d')
site_list = ['caixin','xinhua']
receiver_list = [
    'duanwei_93@163.com',
    'jokerqianli@163.com']
keywords = '比特币 莱特币 以太坊 btc bcc eth 数字货币 虚拟货币 ICO'.split(" ")



def fetch_cache(site = 'caixin'):
    if not os.path.exists("/home/qianli2/GitRepoCollection/bitcoin/cache/{0}/{1}.txt".format(site,date)):
        return dict(),list()
    else:
        res_dic = dict()
        res_list = list()
        with open("/home/qianli2/GitRepoCollection/bitcoin/cache/{0}/{1}.txt".format(site,date)) as file:
            for line in file:
                line_split = line.rstrip("\n").split("||")
                res_dic[line_split[0]] = 1
                res_list.append(line_split)
        return res_dic,res_list

def send_emails(send_dic,receivers=receiver_list):
    content = ''
    for site,lst in send_dic.iteritems():
        content = content+site+"\n"
        for x in lst:
            url, title, time, find_time = x
            content = content+'''
            title:{1}||url:{0}||\ntime:{2}||crawl_time:{3}\n
            '''.format(url,title,time,find_time)
        content = content+'\n'
    for x in receivers:
        send_email(x,content)
    print '*********\nEmails sent\n*********'


if __name__ == '__main__':
    send_dic = dict()
    for site in site_list:
        cache_dic,cache = fetch_cache(site)
        reg_time = ar.now().strftime('%Y/%m/%d %H:%M:%S')
        print '{0} Fetching {1}.'.format(reg_time, site) ,
            # soup = BeautifulSoup(request_page(keyword),'lxml')
            # for item in soup.find_all('div','searchxt'):
            #     url = item.a.get('href')
            #     title = item.a.string.encode("utf-8")
            #     time = item.span.encode("utf-8")[7:17]
                # if not time == date:
                #     continue
        reg_time = ar.now().strftime('%Y/%m/%d %H:%M:%S')
        for url,title,time in yield_info(keywords,site):

            if cache_dic.get(url,0)!=1:
                cache.append([url,title,time,reg_time])
                cache_dic.update({url:1})
                send_dic.setdefault(site,list()).append((url,title,time,reg_time))
                # print url,title,time
                # break
        print ""
        with open('/home/qianli2/GitRepoCollection/bitcoin/cache/{0}/{1}.txt'.format(site, date), 'w') as file:
            for item in sorted(cache, key=lambda x: x[2], reverse=True):
                file.write("||".join(item) + "\n")
    if send_dic:
        send_emails(send_dic=send_dic)


    with open('/home/qianli2/GitRepoCollection/bitcoin/cache/log.txt', 'a') as file:
        file.write("{0} task complete.\n".format(reg_time))

