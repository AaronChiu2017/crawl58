from scrapy_redis.spiders import RedisSpider
from crawl58.items import Crawl58Item
from scrapy.selector import Selector
# from scrapy import log


class Myspider(RedisSpider):
    '''spider that reads urls from redis queue (myspider:start_urls).'''
    name = 'myspider_58'
    redis_key = 'startpage'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Myspider, self).__init__(*args, **kwargs)


    def parse(self, response):
        items=[]
        item=Crawl58Item()
        sel=Selector(response)
        
        phone=sel.xpath('''//span[@class='tel']/i[@class='num']/text()''').extract()
        if len(phone)>0:
            item['phone']=phone[0]
    
        belong=sel.xpath('''//span[@class='belong']/text()''').extract()
        if len(belong)>0:
            item['belong']=belong[0]
            
        name=sel.xpath('''//span[@class='lxr']/a/@title''').extract()
        if len(name)>0:
            item['name']=name[0]

        items.append(item)
        return items





