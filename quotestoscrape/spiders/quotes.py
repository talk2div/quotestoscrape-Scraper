# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urljoin

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']

    script = """
        function main(splash, args)
            splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")
            splash.private_mode_enabled = false
            splash:go(args.url)
            splash:wait(1)
            splash:set_viewport_full()
            return splash:html()
        end
    """
    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com/js',callback=self.parse,endpoint="execute",args={
            'lua_source':self.script
        })

    def parse(self, response):
        row = response.xpath("//div[@class='quote']")
        for each_row in row:
            yield {
                'name':each_row.xpath(".//span[@class='text']/text()").get(),
                'author':each_row.xpath(".//span[2]/small[@class='author']/text()").get()
            }
        next_page = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        url_next = urljoin(response.url,next_page)

        if next_page:
            yield SplashRequest(url=url_next,callback=self.parse,endpoint="execute",args={
            'lua_source':self.script
        })