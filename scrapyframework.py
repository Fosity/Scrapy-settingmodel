# _*_coding:utf-8_*_
# Author:xupan
import queue

from twisted.internet import reactor
from twisted.web.client import getPage, defer


class Response(object):
    '''返回内容，封装爱Response里面'''

    def __init__(self, body, request):
        self.body = body
        self.request = request
        self.url = request.url

    @property
    def text(self):
        return self.body.decode('utf-8')


class Request(object):
    """请求对象"""

    def __init__(self, url, callback=None):
        self.url = url
        self.callback = callback


class Scheduler(object):
    """调度器 是一个队列  存放Request对象"""

    def __init__(self, engine):
        self.q = queue.Queue()
        self.engine = engine

    def enqueue_request(self, request):
        self.q.put(request)

    def next_request(self):
        try:
            req = self.q.get(block=False)
        except Exception as e:
            req = None

        return req

    def size(self):
        return self.q.qsize()


class ExecutionEngine(object):
    """引擎"""

    def __init__(self):
        self._closewait = None
        self.running = True
        self.start_requests = None  # 起始的网址 ，可以是列表
        self.scheduler = Scheduler(self)  # 创建调度器对象

        self.inprogress = set()  # 正在执行的 任务 集合

    def check_empty(self, response):
        # 断开机制，如果工作状态为False的话，那么 一直执行的_closewait的任务就有返回值，然后离开结束
        if not self.running:
            self._closewait.callback('......')

    def _next_request(self):
        """
        执行的主函数
        1. 如果有起始函数，全部取出来，放在调度器中，直到没有。
        2. 如果正在执行任务小于5（为了限制并发数）以及调度器中有任务的时候，就会从调度器中读取 Request对象，在正在任务集合中写入，然后创建连接，
        3. 当 连接有内容的时候，不管正确，错误，都会执行回调函数。1.有值，2.从正在执行任务集合中删除，3，在执行自己函数。
        4. 如果没有正在执行任务，以及 调度器中没有任务，那么 一直执行的_closewait的任务就有返回值，然后离开结束
        """
        while self.start_requests:
            try:
                request = next(self.start_requests)
            except StopIteration:
                self.start_requests = None
            else:
                self.scheduler.enqueue_request(request)

        while len(self.inprogress) < 5 and self.scheduler.size() > 0:  # 最大并发数为5

            request = self.scheduler.next_request()
            if not request:
                break

            self.inprogress.add(request)
            d = getPage(bytes(request.url, encoding='utf-8'))
            d.addBoth(self._handle_downloader_output, request)
            d.addBoth(lambda x, req: self.inprogress.remove(req), request)
            d.addBoth(lambda x: self._next_request())

        if len(self.inprogress) == 0 and self.scheduler.size() == 0:
            self._closewait.callback(None)

    def _handle_downloader_output(self, body, request):
        """
        获取内容，执行回调函数，并且把回调函数中的返回值获取，并添加到队列中
        :param response:
        :param request:
        :return:
        """
        import types

        response = Response(body, request)
        func = request.callback or self.spider.parse
        gen = func(response)
        if isinstance(gen, types.GeneratorType):
            # 判断是否是迭代器
            for req in gen:
                self.scheduler.enqueue_request(req)

    @defer.inlineCallbacks
    def start(self):
        # 这个就是一直 在运行的 任务
        self._closewait = defer.Deferred()
        yield self._closewait

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests):
        # 入口234
        self.start_requests = start_requests  # 把起始网址 传到engine
        self.spider = spider  # 把 自己定义的类传到engine
        yield None  # 没有任何作用，
        reactor.callLater(0, self._next_request)  # yield，之后多久执行这个函数 ，0是多少秒以后


class Crawler(object):
    def __init__(self, spidercls):
        self.spidercls = spidercls

        self.spider = None
        self.engine = None

    @defer.inlineCallbacks
    def crawl(self):
        # 入口123 到这里
        self.engine = ExecutionEngine()  # 实例化引擎对象
        self.spider = self.spidercls()  # 实力化 自己写得搜索类对象
        start_requests = iter(self.spider.start_requests())  # 网址的对象 Request迭代器 从Spider类中来
        yield self.engine.open_spider(self.spider, start_requests)  # 自己定义的运行任务  入口234
        yield self.engine.start()  # 产生一直运行的任务，入口


class CrawlerProcess(object):
    def __init__(self):
        self._active = set()
        self.crawlers = set()

    def crawl(self, spidercls, *args, **kwargs):
        crawler = Crawler(spidercls)  # 对于每一个起始url 产生一个对象
        self.crawlers.add(crawler)  # 去重

        d = crawler.crawl(*args, **kwargs)  # 返回一个deffer对象  #这里是每个url执行的入口123
        self._active.add(d)  # 增加deffer对象到 集合中
        return d

    def start(self):
        dl = defer.DeferredList(self._active)
        dl.addBoth(self._stop_reactor)  # 所有的爬虫终止 调用
        reactor.run()

    def _stop_reactor(self, _=None):
        reactor.stop()


class Spider(object):
    '''循环开始的url 封装成Request迭代对象'''

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)


class ChoutiSpider(Spider):
    name = "chouti"
    start_urls = [
        'http://dig.chouti.com/',
    ]

    def parse(self, response):
        print(response.text)


class CnblogsSpider(Spider):
    name = "cnblogs"
    start_urls = [
        'http://www.cnblogs.com/',
    ]

    def parse(self, response):
        print(response.text)


if __name__ == '__main__':

    spider_cls_list = [ChoutiSpider, CnblogsSpider]

    crawler_process = CrawlerProcess()  #
    for spider_cls in spider_cls_list:
        crawler_process.crawl(spider_cls)

    crawler_process.start()
