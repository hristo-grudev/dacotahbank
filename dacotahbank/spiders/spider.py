import scrapy

from scrapy.loader import ItemLoader

from ..items import DacotahbankItem
from itemloaders.processors import TakeFirst


class DacotahbankSpider(scrapy.Spider):
	name = 'dacotahbank'
	start_urls = ['https://www.dacotahbank.com/newsroom']

	def parse(self, response):
		post_links = response.xpath('//a[text()="Read More"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="pager-next last"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="field-items"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="article-date"]//text()').get()

		item = ItemLoader(item=DacotahbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
