from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
import MySQLdb

class Cox_kings(BaseSpider):
    name = 'coxkings'
    start_urls = ['http://www.coxandkings.com/bharatdeko/north-india/','http://www.coxandkings.com/bharatdeko/south-india/','http://www.coxandkings.com/bharatdeko/west-india/', 'http://www.coxandkings.com/bharatdeko/east-india/', 'http://www.coxandkings.com/bharatdeko/central-india/']

    def __init__(self, *args, **kwargs):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd='01491a0237db', db="kingsdb", charset='utf8', use_unicode = True)
        self.cur = self.conn.cursor()
    
    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//div[@id="pacakage_container_bd"]/div[contains(@id, "table")]')
        for node in nodes:
            title = ''.join(node.xpath('./div[@class="floatl"]//div[@class="floatl padr5"]/h4/text()').extract()) 
            daynyt = ''.join(node.xpath('./div[@class="floatl"]//div[@class="floatl bd_days"]/text()').extract())
            cost = ''.join(node.xpath('./div[@class="floatl"]//div[@class="price"]/text()').extract())
            qry = 'insert into kings(title, daynyt_1, cost_1) values (%s, %s, %s)on duplicate key update title = %s'
            values = (title, daynyt, cost, title)
            print qry%values
            self.cur.execute(qry, values)
            self.conn.commit()

