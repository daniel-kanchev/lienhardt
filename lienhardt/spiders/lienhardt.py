import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from lienhardt.items import Article


class LienhardtSpider(scrapy.Spider):
    name = 'lienhardt'
    start_urls = ['https://www.lienhardt.ch/beitragsarchiv/']

    def parse(self, response):
        links = response.xpath('//div[@class="col-xs-4 right"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2//text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//div[@class="blog-detail-wrap"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
