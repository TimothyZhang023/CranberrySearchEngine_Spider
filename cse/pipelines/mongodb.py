import datetime
import traceback

__author__ = 'TianShuo'
from pymongo import MongoClient
from scrapy import log
import time


class SingleMongodbPipeline(object):
    """
        save the data to mongodb.
    """

    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DB = "html"

    def __init__(self):
        """
            The only async framework that PyMongo fully supports is Gevent.

            Currently there is no great way to use PyMongo in conjunction with Tornado or Twisted. PyMongo provides built-in connection pooling, so some of the benefits of those frameworks can be achieved just by writing multi-threaded code that shares a MongoClient.
        """

        try:
            client = MongoClient(self.MONGODB_SERVER, self.MONGODB_PORT)
            self.db = client[self.MONGODB_DB]
        except Exception as e:
            log.msg("ERROR(SingleMongodbPipeline): %s" % (str(e),), log.ERROR)
            traceback.print_exc()

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('SINGLE_MONGODB_SERVER', 'localhost')
        cls.MONGODB_PORT = crawler.settings.getint('SINGLE_MONGODB_PORT', 27017)
        cls.MONGODB_DB = crawler.settings.get('SINGLE_MONGODB_DB', 'html')
        print cls.MONGODB_SERVER, cls.MONGODB_PORT, cls.MONGODB_DB
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def process_item(self, item, spider):
        html_detail = {
            'docId': item.get('url_id'),
            'url': item.get('url', ''),
            'content': item.get('content', ''),
            'encoding': item.get('encoding', ''),
            'update_time': time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        result = self.db['html_detail'].delete_one({'docId': item.get('url_id')})
        result = self.db['html_detail'].save(html_detail)

        print ("save in mongodb:" + item['url'])

        return item
