# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class SpmodelSpiderMiddleware(object):
	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the spider middleware does not modify the
	# passed objects.

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_spider_input(self, response, spider):
		# Called for each response that goes through the spider
		# middleware and into the spider.

		# Should return None or raise an exception.
		return None

	def process_spider_output(self, response, result, spider):
		# Called with the results returned from the Spider, after
		# it has processed the response.

		# Must return an iterable of Request, dict or Item objects.
		for i in result:
			yield i

	def process_spider_exception(self, response, exception, spider):
		# Called when a spider or process_spider_input() method
		# (from other spider middleware) raises an exception.

		# Should return either None or an iterable of Response, dict
		# or Item objects.
		pass

	def process_start_requests(self, start_requests, spider):
		# Called with the start requests of the spider, and works
		# similarly to the process_spider_output() method, except
		# that it doesn’t have a response associated.

		# Must return only requests (not items).
		for r in start_requests:
			yield r

	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)


class SpmodelDownloaderMiddleware(object):
	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the downloader middleware does not modify the
	# passed objects.

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_request(self, request, spider):
		# Called for each request that goes through the downloader
		# middleware.

		# Must either:
		# - return None: continue processing this request
		# - or return a Response object
		# - or return a Request object
		# - or raise IgnoreRequest: process_exception() methods of
		#   installed downloader middleware will be called
		return None

	def process_response(self, request, response, spider):
		# Called with the response returned from the downloader.

		# Must either;
		# - return a Response object
		# - return a Request object
		# - or raise IgnoreRequest
		return response

	def process_exception(self, request, exception, spider):
		# Called when a download handler or a process_request()
		# (from other downloader middleware) raises an exception.

		# Must either:
		# - return None: continue processing this exception
		# - return a Response object: stops process_exception() chain
		# - return a Request object: stops process_exception() chain
		pass

	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)



######代理 方案二 #####
###需要在setting下载中间件中配置###
def to_bytes(text, encoding=None, errors='strict'):
	import six
	if isinstance(text, bytes):
		return text
	if not isinstance(text, six.string_types):
		raise TypeError('to_bytes must receive a unicode, str or bytes '
						'object, got %s' % type(text).__name__)
	if encoding is None:
		encoding = 'utf-8'
	return text.encode(encoding, errors)


class ProxyMiddleware(object):

	def process_request(self, request, spider):
		import random
		import base64
		PROXIES = [
			{'ip_port': '111.11.228.75:80', 'user_pass': ''},
			{'ip_port': '120.198.243.22:80', 'user_pass': ''},
			{'ip_port': '111.8.60.9:8123', 'user_pass': ''},
			{'ip_port': '101.71.27.120:80', 'user_pass': ''},
			{'ip_port': '122.96.59.104:80', 'user_pass': ''},
			{'ip_port': '122.224.249.122:8088', 'user_pass': ''},
		]
		proxy = random.choice(PROXIES)
		if proxy['user_pass'] is not None:
			request.meta['proxy'] = to_bytes("http://%s" % proxy['ip_port'])
			encoded_user_pass = base64.encodestring(to_bytes(proxy['user_pass']))
			request.headers['Proxy-Authorization'] = to_bytes('Basic ' + encoded_user_pass)
			print(
				"**************ProxyMiddleware have pass************" + proxy['ip_port'])
		else:
			print(
				"**************ProxyMiddleware no pass************" + proxy['ip_port'])
			request.meta['proxy'] = to_bytes("http://%s" % proxy['ip_port'])
