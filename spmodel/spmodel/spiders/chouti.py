# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector


class ChoutiSpider(scrapy.Spider):
	name = 'chouti'
	allowed_domains = ['chouti.com']
	start_urls = ['http://chouti.com/']
	cookie_dict = {}


	def start_requests(self):
		for url in self.start_urls:
			yield Request(url,dont_filter=True,callback=self.login)
	def login(self,response):
		from scrapy.http.cookies import CookieJar
		cookie_jar=CookieJar()
		cookie_jar.extract_cookies(response,response.request)

		for k,v in cookie_jar._cookies.items():
			for i,j in v.items():
				for m,n in j.items():
					self.cookie_dict[m]=n.value

		post_dict={
			"phone": "8618001999999",
			"password":"qqqwwwxxx",
			"oneMonth":1,
		}

		import urllib.parse

		yield Request(
			url="http://dig.chouti.com/login",
			method='POST',
			cookies=self.cookie_dict,
			body=urllib.parse.urlencode(post_dict),
			headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
			callback=self.parse1
		)


	def parse1(self,response):
		yield Request(url='http://dig.chouti.com/',cookies=self.cookie_dict,callback=self.parse)

	def parse(self, response):
		hxs = Selector(response)
		link_id_list = hxs.xpath('//div[@class="part2"]/@share-linkid').extract()
		print(link_id_list)
		for link_id in link_id_list:
			# 获取每一个ID去点赞
			base_url = "http://dig.chouti.com/link/vote?linksId=%s" % (link_id,)
			yield Request(url=base_url, method="POST", cookies=self.cookie_dict, callback=self.parse2)

		page_list = hxs.xpath('//div[@id="dig_lcpage"]//a/@href').extract()
		for page in page_list:
			# http://dig.chouti.com/ /all/hot/recent/2
			page_url = "http://dig.chouti.com%s" % (page,)
			yield Request(url=page_url, method='GET', callback=self.parse)

	def parse2(self, response):
		print(response.text)