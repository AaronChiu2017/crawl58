#coding=utf-8
from scrapy_redis.spiders import RedisSpider
from redis import Redis
from scrapy import log
from time import sleep
from scrapy.selector import Selector
class Myspider(RedisSpider):
    '''spider that reads urls from redis queue (myspider:start_urls).'''
    name = 'myspider_58page'
    redis_key = 'urls58'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Myspider, self).__init__(*args, **kwargs)
        self.url = 'http://bj.58.com'

    def parse(self, response):
        sel=Selector(response)
        #print sel.extract()
        board= sel.xpath('''//div[@class="board"]''')
        urls_temp=[]
        urls=[]
        if len(board) > 0:
            urls_temp.extend(board[0].xpath('''.//a/@href''').extract())
        if len(urls_temp) != 0:
            for url in urls_temp:
                if 'http' in url:
                    urls.append(url)
                else:
                    urls.append(self.url+url)
            r=Redis()
            print 'first blood'
            for url in urls:
                print url
                r.lpush('urls58',url)
        if len(urls_temp) == 0:
            sel2=Selector(response)
            urls2=[]
            urls2.extend(sel2.xpath('''//td[@class='t']/a/@href''').extract())
            print 'second blood'
            r=Redis()
            for url in urls2:
                if 'http' in url and 'zhiding' not in url:
                    print url
                    r.lpush('startpage',url)
                
