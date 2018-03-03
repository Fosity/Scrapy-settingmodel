# -*- coding: utf-8 -*-

# Scrapy settings for spmodel project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

#1.爬虫名称 ：看对方是否允许
BOT_NAME = 'spmodel'

#2.爬虫应用路径
SPIDER_MODULES = ['spmodel.spiders']
NEWSPIDER_MODULE = 'spmodel.spiders'


#3.客户端 User-agent 请求头 ：浏览器是什么设备！
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spmodel (+http://www.yourdomain.com)'


#4.禁止爬虫配置
# Obey robots.txt rules
ROBOTSTXT_OBEY = True


#5.并发请求数
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32


#6.延迟下载秒数
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3


#7.单域名访问并发数，并且延迟下次秒数也应用在每个域名
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#单IP访问并发数，如果有值则忽略：CONCURRENT_REQUESTS_PER_DOMAIN ，并且延迟下次秒数也yingy在每个IP
#CONCURRENT_REQUESTS_PER_IP = 16


#8.是否支持cookie，cookiejar进行操作cookie
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False
#COOKIES_DEBUG=True


#9.Telent用于查看当前爬虫的信息，操作爬虫等。。。
#  使用telnet ip port ，然后通过命令操作
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False
#TELNETCONSOLE_ENABLED=True
#TELNETCONSOLE_HOST='127.0.0.1'
#TELNETCONSOLE_PORT=[6023,]


#10.默认请求头
# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

##爬虫中间件
"""
class SpiderMiddleware(object):

	def process_spider_input(self, response, spider):
		'''
		下载完成，执行，然后交给parse处理
		:param response: 
		:param spider: 
		:return: 
		'''
		pass

	def process_spider_output(self, response, result, spider):
		'''
		spider处理完成，返回时调用
		:param response:
		:param result:
		:param spider:
		:return: 必须返回包含 Request 或 Item 对象的可迭代对象(iterable)
		'''
		return result

	def process_spider_exception(self, response, exception, spider):
		'''
		异常调用
		:param response:
		:param exception:
		:param spider:
		:return: None,继续交给后续中间件处理异常；含 Response 或 Item 的可迭代对象(iterable)，交给调度器或pipeline
		'''
		return None

	def process_start_requests(self, start_requests, spider):
		'''
		爬虫启动时调用
		:param start_requests:
		:param spider:
		:return: 包含 Request 对象的可迭代对象
		'''
		return start_requests


内置爬虫中间件：
'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware': 50,
'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': 500,
'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': 700,
'scrapy.contrib.spidermiddleware.urllength.UrlLengthMiddleware': 800,
'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': 900,

"""
# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'spmodel.middlewares.SpmodelSpiderMiddleware': 543,
#}


#下载中间件
"""
    class DownMiddleware1(object):
        def process_request(self, request, spider):
            '''
            请求需要被下载时，经过所有下载器中间件的process_request调用
            :param request:
            :param spider:
            :return:
                None,继续后续中间件去下载；
                Response对象，停止process_request的执行，开始执行process_response
                Request对象，停止中间件的执行，将Request重新调度器
                raise IgnoreRequest异常，停止process_request的执行，开始执行process_exception
            '''
            pass
        def process_response(self, request, response, spider):
            '''
            spider处理完成，返回时调用
            :param response:
            :param result:
            :param spider:
            :return:
                Response 对象：转交给其他中间件process_response
                Request 对象：停止中间件，request会被重新调度下载
                raise IgnoreRequest 异常：调用Request.errback
            '''
            print('response1')
            return response

        def process_exception(self, request, exception, spider):
            '''
            当下载处理器(download handler)或 process_request() (下载中间件)抛出异常
            :param response:
            :param exception:
            :param spider:
            :return:
                None：继续交给后续中间件处理异常；
                Response对象：停止后续process_exception方法
                Request对象：停止中间件，request将会被重新调用下载
            '''
            return None

    默认下载中间件
    {
        'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
        'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
        'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
        'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
        'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
        'scrapy.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': 580,
        'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 590,
        'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
        'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
        'scrapy.contrib.downloadermiddleware.chunked.ChunkedTransferMiddleware': 830,
        'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
        'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900,
    }
"""
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'spmodel.middlewares.SpmodelDownloaderMiddleware': 543,
#}


#12.自定义扩展，基于信号调用
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


#11.定义pipeline处理请求 300-1000
# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'spmodel.pipelines.SpmodelPipeline': 300,
#}

#13.爬虫允许的最大深度，可以通过meta查看当前深度：0表示无深度
# DEPTH_LIMIT=3


#14.爬虫时，0表示深度优先Lifo（默认）；1表示广度优先FiFo

#后进先出，深度优先
#DEPTH_PRIORITY=0
#SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleLifoDiskQueue'
#SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.LifoMemoryQueue'

#先进先出，广度优先
#DEPTH_PRIORITY=1
#SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleLifoDiskQueue'
#SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.LifoMemoryQueue'

#15 调度器队列
#SCHEDULER = 'scrapy.core.scheduler.Scheduler'
#from scrapy.core.scheduler import Scheduler


#16 访问URL去重
# DUPEFILTER_CLASS = '自定义去重'

"""
17. 自动限速算法
    from scrapy.contrib.throttle import AutoThrottle
    自动限速设置
    1. 获取最小延迟 DOWNLOAD_DELAY
    2. 获取最大延迟 AUTOTHROTTLE_MAX_DELAY
    3. 设置初始下载延迟 AUTOTHROTTLE_START_DELAY
    4. 当请求下载完成后，获取其"连接"时间 latency，即：请求连接到接受到响应头之间的时间
    5. 用于计算的... AUTOTHROTTLE_TARGET_CONCURRENCY
    target_delay = latency / self.target_concurrency
    new_delay = (slot.delay + target_delay) / 2.0 # 表示上一次的延迟时间
    new_delay = max(target_delay, new_delay)
    new_delay = min(max(self.mindelay, new_delay), self.maxdelay)
    slot.delay = new_delay
"""

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# 开始自动限速
#AUTOTHROTTLE_ENABLED = True

# The initial download delay
# 初始下载延迟
#AUTOTHROTTLE_START_DELAY = 5

# The maximum download delay to be set in case of high latencies
# 最大下载延迟
#AUTOTHROTTLE_MAX_DELAY = 60

# The average number of requests Scrapy should be sending in parallel to each remote server
#平均每秒并发数
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Enable showing throttling stats for every response received:
#是否显示
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
"""
18. 启用缓存
    目的用于将已经发送的请求或相应缓存下来，以便以后使用
    from scrapy.downloadermiddlewares.httpcache import HttpCacheMiddleware
    from scrapy.extensions.httpcache import DummyPolicy
    from scrapy.extensions.httpcache import FilesystemCacheStorage
"""
# 是否启用缓存策略
#HTTPCACHE_ENABLED = True

# 缓存策略：所有请求均缓存，下次在请求直接访问原来的缓存即可
# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.DummyPolicy"
# 缓存策略：根据Http响应头：Cache-Control、Last-Modified 等进行缓存的策略
# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.RFC2616Policy"

# 缓存超时时间
#HTTPCACHE_EXPIRATION_SECS = 0

# 缓存保存路径
#HTTPCACHE_DIR = 'httpcache'

# 缓存忽略的Http状态码
#HTTPCACHE_IGNORE_HTTP_CODES = []

# 缓存存储的插件
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 19. 代理，需要在环境变量中设置
"""
    from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware

    方式一：使用默认
        os.environ
        {
            http_proxy:http://root:woshiniba@192.168.11.11:9999/
            https_proxy:http://192.168.11.11:9999/
        }
    方式二：使用自定义下载中间件

    def to_bytes(text, encoding=None, errors='strict'):
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
                request.meta['proxy'] = to_bytes（"http://%s" % proxy['ip_port']）
                encoded_user_pass = base64.encodestring(to_bytes(proxy['user_pass']))
                request.headers['Proxy-Authorization'] = to_bytes('Basic ' + encoded_user_pass)
                print "**************ProxyMiddleware have pass************" + proxy['ip_port']
            else:
                print "**************ProxyMiddleware no pass************" + proxy['ip_port']
                request.meta['proxy'] = to_bytes("http://%s" % proxy['ip_port'])

    DOWNLOADER_MIDDLEWARES = {
       'step8_king.middlewares.ProxyMiddleware': 500,
    }

"""

#20. Https访问 自定义证书
"""
    Https访问时有两种情况：
    1. 要爬取网站使用的可信任证书(默认支持)
        DOWNLOADER_HTTPCLIENTFACTORY = "scrapy.core.downloader.webclient.ScrapyHTTPClientFactory"
        DOWNLOADER_CLIENTCONTEXTFACTORY = "scrapy.core.downloader.contextfactory.ScrapyClientContextFactory"

    2. 要爬取网站使用的自定义证书
        DOWNLOADER_HTTPCLIENTFACTORY = "scrapy.core.downloader.webclient.ScrapyHTTPClientFactory"
        DOWNLOADER_CLIENTCONTEXTFACTORY = "step8_king.https.MySSLFactory"  #可以自定义

        # https.py
        from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory
        from twisted.internet.ssl import (optionsForClientTLS, CertificateOptions, PrivateCertificate)

        class MySSLFactory(ScrapyClientContextFactory):
            def getCertificateOptions(self):
                from OpenSSL import crypto
                #加密证书
                v1 = crypto.load_privatekey(crypto.FILETYPE_PEM, open('/client.key.unsecure', mode='r').read())
                v2 = crypto.load_certificate(crypto.FILETYPE_PEM, open('/client.pem', mode='r').read())
                
                return CertificateOptions(
                    privateKey=v1,  # pKey对象
                    certificate=v2,  # X509对象
                    verify=False,
                    method=getattr(self, 'method', getattr(self, '_ssl_method', None))
                )
    其他：
        相关类
            scrapy.core.downloader.handlers.http.HttpDownloadHandler
            scrapy.core.downloader.webclient.ScrapyHTTPClientFactory
            scrapy.core.downloader.contextfactory.ScrapyClientContextFactory
        相关配置
            DOWNLOADER_HTTPCLIENTFACTORY
            DOWNLOADER_CLIENTCONTEXTFACTORY

"""