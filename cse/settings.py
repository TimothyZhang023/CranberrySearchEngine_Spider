#!/usr/bin/python
#-*-coding:utf-8-*-

# Scrapy settings for cse project
import os

BOT_NAME = 'cse'

SPIDER_MODULES = ['cse.spiders']
NEWSPIDER_MODULE = 'cse.spiders'

DOWNLOAD_TIMEOUT = 20
DOWNLOAD_DELAY = 0
CONCURRENT_ITEMS = 50
CONCURRENT_REQUESTS = 100

#The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single domain.
CONCURRENT_REQUESTS_PER_DOMAIN = 1000
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
    'cse.pipelines.save_html.SaveHtmlPipeline': 900,
    'cse.pipelines.notify.IndexNotifyPipeline': 901,
}

COOKIES_ENABLED = False

#USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31'

DOWNLOADER_MIDDLEWARES = {
    #    'cse.contrib.downloadmiddleware.google_cache.GoogleCacheMiddleware':50,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'cse.contrib.downloadmiddleware.rotate_useragent.RotateUserAgentMiddleware': 400,
    'cse.contrib.downloadmiddleware.filter_responses.FilterResponses': 999,
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

ALLOWED_DOMAIN = [
    'njtech.edu.cn',
    'njut.asia',
    '127.0.0.1',
]

LOG_FILE = "scrapy.log"
LOG_LEVEL = "INFO"
LOG_STDOUT = False

#STATS_CLASS = ''

'''
Notice , SpiderPriorityQueue is not supported by Redis Cluster use SpiderQueue or SpiderStack Instead~
'''
#DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'
#SCHEDULER = 'scrapy.core.scheduler.Scheduler'
SCHEDULER = "cse.scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = False
SCHEDULER_QUEUE_CLASS = 'cse.scrapy_redis.queue.SpiderPriorityQueue'
# JOBDIR='jobs'


#AJAXCRAWL_ENABLED = True

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

REDIS_HOST_Notify = "127.0.0.1"
REDIS_PORT_Notify = 6379


#Index Notify Queue Key
IndexNotifyQueue = "IndexNotifyQueue"

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
HTML_DIR = os.path.join(PROJECT_DIR, '../html')
