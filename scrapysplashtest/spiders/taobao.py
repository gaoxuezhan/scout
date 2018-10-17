# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urllib.parse import quote
from scrapysplashtest.items import ProductItem
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
import datetime

script = """
function main(splash, args)
  splash:set_user_agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  return splash:html()
end
"""


class TaobaoSpider(Spider):
    name = 'taobao'
    allowed_domains = ['www.tianxun.com']
    base_url = 'https://s.taobao.com/search?q='
    url = 'https://www.tianxun.com/oneway-pek-cszx.html?depdate=2018-11-03&cabin=Economy'

    def start_requests(self):
        # for keyword in self.settings.get('KEYWORDS'):
        #     for page in range(1, self.settings.get('MAX_PAGE') + 1):
        #         url = self.base_url + quote(keyword)
        #         yield SplashRequest(url, callback=self.parse, endpoint='execute',
        #                             args={'lua_source': script, 'page': page, 'wait': 7})
        yield SplashRequest(self.url, callback=self.parse, endpoint='execute',
                            args={'lua_source': script,  'wait': 0.5})

    def parse(self, response):
        # print('gaoxz1:' + str(response.text))
        # print('gaoxz2:' + str(type(response)))
        # products = response.xpath(
        #     '//div[@class="list_con"]')
        # for product in products:
        #     item = ProductItem()
        #     item['price'] = ''.join(product.xpath('.//div[contains(@class, "price")]//text()').extract()).strip()
        #     item['title'] = ''.join(product.xpath('.//div[contains(@class, "title")]//text()').extract()).strip()
        #     item['shop'] = ''.join(product.xpath('.//div[contains(@class, "shop")]//text()').extract()).strip()
        #     item['image'] = ''.join(
        #         product.xpath('.//div[@class="pic"]//img[contains(@class, "img")]/@data-src').extract()).strip()
        #     item['deal'] = product.xpath('.//div[contains(@class, "deal-cnt")]//text()').extract_first()
        #     item['location'] = product.xpath('.//div[contains(@class, "location")]//text()').extract_first()
        #     yield item

        # ouput -> All
        soup = BeautifulSoup(response.body, from_encoding="utf-8")

        # ouput -> attrs={"ui-view": "content"}
        soup = soup.select(".list_con")
        for s in soup:
            # print(s.text)
            # print(str(s))
            # print(s.select('div.box1 > span.fl.airline')[0].text)
            # # print(s.select('div.box1 > span.fl.airline > b')[0].text)
            # # print(s.select('div.box1 > span.fl.airline > b')[0].decompose())
            #
            # print(s.select('div.box2 > p')[0].text)
            # print(s.select('div.box2 > span')[0].text)
            # print(s.select('div.box3.fl.ac > p.timeBox')[0].text)
            # print(s.select('div.box3 > p.oneWay.runBox')[0].text)
            item = ProductItem()

            if(len(s.select('div.box1 > span.fl.airline > b')) > 0):
                item['code'] = s.select('div.box1 > span.fl.airline > b')[0].text
                s.select('div.box1 > span.fl.airline > b')[0].decompose()
            else:
                item['code'] = s.select('div.box1 > span.fl.airline > span > b')[0].text
                s.select('div.box1 > span.fl.airline > span > b')[0].decompose()

            item['company'] = s.select('div.box1 > span.fl.airline')[0].text
            item['departureTime'] = s.select('div.box2 > p')[0].text
            item['departureAirport'] = s.select('div.box2 > span')[0].text
            item['timeCost'] = s.select('div.box3.fl.ac > p.timeBox')[0].text
            item['type'] = s.select('div.box3 > p.oneWay.runBox')[0].text
            item['arriveTime'] = s.select('div.box4 > p')[0].text
            item['arriveAirport'] = s.select('div.box4 > span')[0].text
            item['price'] = s.select('.pricefield')[0].text
            item['updateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield item

        if len(soup) < 1:
            print('"No body here! I must go back to get it again!"')
            yield SplashRequest(self.url, callback=self.parse, endpoint='execute',
                                args={'lua_source': script, 'wait': 0.5}, dont_filter=True)
        else:
            print('"Mission complete! Waiting for next time! Over!"')