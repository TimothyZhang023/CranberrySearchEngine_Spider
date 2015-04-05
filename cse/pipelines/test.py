#!/usr/bin/python
#-*-coding:utf-8-*-

from scrapy import log
import scrapy
from cse.scrapy_redis.queue import IndexNotifyQueue

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_HOST_Notify = 'localhost'
REDIS_PORT_Notify = 6379


class TestPipeline(object):
    """
        This only for print the final item for the purpose of debug,because the default
        scrapy output the result,so if you use this pipeline,you better change the scrapy
        source code:
        
        sudo vim /usr/local/lib/python2.7/dist-packages/Scrapy-0.16.4-py2.7.egg/scrapy/core/scrapy.py
        make line 211 like this:
            #log.msg(level=log.DEBUG, spider=spider, **logkws)
    """

    def __init__(self, server, port, key):
        self.server = server
        self.port = port
        self.key = key

        pass


    @classmethod
    def from_settings(cls, settings):
        server = settings.get('REDIS_HOST_Notify', REDIS_HOST)
        port = settings.get('REDIS_PORT_Notify', REDIS_PORT)
        key = settings.get('IndexNotifyQueue', 'IndexNotifyQueue')
        return cls(server, port, key)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls.from_settings(settings)


    def process_item(self, item, spider):
        #print self.style.NOTICE("SUCCESS(item):" + item['original_url'])

        #print "Test Pipeline process item:", item

        filename = 'html/' + item['redis_id'] + '.html'
        open(filename, 'wb').write(item['content'])

        index_notify = {
            'hash_key': item['redis_id'],
            'url': item['url'],
            'title': item['title'],
            'page_encoding': item['encoding'],
            'storage_type': 'local_fs',
            'queue_time': item['fetch_time']
        }

        index_notify_queue = IndexNotifyQueue(self.server, self.port, self.key)
        index_notify_queue.push(index_notify)

        return item

    def handle_error(self, e):
        log.err(e)

