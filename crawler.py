#-*-coding:utf-8-*-
import urllib
import re
import time

source = 'http://finance.people.com.cn/'
data = urllib.urlopen(source)
txt = data.read()
year = time.strftime("%Y",time.localtime())
date = time.strftime("%m%d",time.localtime())
print date
reg_exp = '''href='(/n1/'''+year+'/'+date+'/c'+'.+?'+'''\.html)' target="_blank">'''
print reg_exp
article_ids = re.findall(reg_exp,txt)
article_urls = ['http://finance.people.com.cn' + article_id for article_id in article_ids]
print article_urls[:5]
