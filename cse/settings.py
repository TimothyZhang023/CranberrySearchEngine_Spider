#!/usr/bin/python
#-*-coding:utf-8-*-

# Scrapy settings for cse project
import os

BOT_NAME = 'cse'

SPIDER_MODULES = ['cse.spiders']
NEWSPIDER_MODULE = 'cse.spiders'

DOWNLOAD_TIMEOUT = 60
DOWNLOAD_DELAY = 0
CONCURRENT_ITEMS = 200
CONCURRENT_REQUESTS = 500

#The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single domain.
CONCURRENT_REQUESTS_PER_DOMAIN = 20
CONCURRENT_REQUESTS_PER_IP = 0
DEPTH_LIMIT = 0
DEPTH_PRIORITY = 0

DNSCACHE_ENABLED = True
RETRY_ENABLED = False


#AutoThrottle extension
AUTOTHROTTLE_ENABLED = False
AUTOTHROTTLE_START_DELAY = 3.0
AUTOTHROTTLE_CONCURRENCY_CHECK_PERIOD = 10  #How many responses should pass to perform concurrency adjustments.

#XXX:scrapy's item pipelines have orders!!!!!,it will go through all the pipelines by the order of the list;
#So if you change the item and return it,the new item will transfer to the next pipeline.
ITEM_PIPELINES = {
   # 'cse.pipelines.local_fs.SaveHtmlPipeline': 900,
    'cse.pipelines.mongodb.SingleMongodbPipeline': 901,
    'cse.pipelines.redis.IndexNotifyPipeline': 902,

}

COOKIES_ENABLED = False

#USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31'

DOWNLOADER_MIDDLEWARES = {
    #    'cse.contrib.downloadmiddleware.google_cache.GoogleCacheMiddleware':50,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'cse.contrib.downloadmiddleware.rotate_useragent.RotateUserAgentMiddleware': 400,
    'cse.contrib.downloadmiddleware.filter_responses.FilterResponses': 999,
}

SPIDER_MIDDLEWARES_BASE={
     'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
     'cse.contrib.spidermiddleware.njtech_offsite.NjtechOffsiteMiddleware':500
}


#To make RotateUserAgentMiddleware enable.
USER_AGENT = ''


#For more mime types about file,you can visit:
#http://mimeapplication.net/
HTML_FILE_CONTENT_TYPE = [
    'text/xml',
    'text/html',
    'text/plain',
]


LOG_FILE = "scrapy.log"
LOG_LEVEL = "ERROR"
LOG_STDOUT = False

SCHEDULER = "cse.scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = False
SCHEDULER_QUEUE_CLASS = 'cse.scrapy_redis.queue.SpiderQueue'

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

REDIS_HOST_NOTIFY = "127.0.0.1"
REDIS_PORT_NOTIFY = 6379

SINGLE_MONGODB_SERVER = "127.0.0.1"
SINGLE_MONGODB_PORT = 27017
SINGLE_MONGODB_DB = "html"


INDEX_NOTIFY_KEY = "IndexNotifyQueue"

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
HTML_DIR = os.path.join(PROJECT_DIR, '../html')


# JOBDIR='jobs'

#AJAXCRAWL_ENABLED = True

#STATS_CLASS = ''

#DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'
#SCHEDULER = 'scrapy.core.scheduler.Scheduler'