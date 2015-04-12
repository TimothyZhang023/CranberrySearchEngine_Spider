#!/usr/bin/python
#-*-coding:utf-8-*-

from scrapy import log
import time
from cse.scrapy_redis.queue import IndexNotifyQueue

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_HOST_NOTIFY = 'localhost'
REDIS_PORT_NOTIFY = 6379


class IndexNotifyPipeline(object):
    def __init__(self, server, port, key, settings):
        self.server = server
        self.port = port
        self.key = key
        self.settings = settings

        pass

    @classmethod
    def from_settings(cls, settings):
        server = settings.get('REDIS_HOST_NOTIFY', REDIS_HOST)
        port = settings.get('REDIS_PORT_NOTIFY', REDIS_PORT)
        key = settings.get('INDEX_NOTIFY_KEY', 'IndexNotifyQueue')
        return cls(server, port, key, settings)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls.from_settings(settings)

    def process_item(self, item, spider):
        index_notify = {
            'hash_key': item['url_id'],
            'url': item['url'],
            'title': item['title'],
            'page_encoding': item['encoding'],
            'storage_type': 'local_fs',
            'storage_position': self.settings.get('HTML_DIR', REDIS_HOST),
            'queue_time': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        index_notify_queue = IndexNotifyQueue(self.server, self.port, self.key)
        index_notify_queue.push(index_notify)

        return item

    def handle_error(self, e):
        log.err(e)

