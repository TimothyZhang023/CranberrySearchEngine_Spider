#!/usr/bin/python
#-*-coding:utf-8-*-

"""
    After you run the project every time,the stats infomation in still in the redis database.
    
    Run this file can help you clear the stats in the redis database.
"""

import redis

# default values
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
STATS_KEY = 'scrapy:stats'
REQUESRTS_KEY = 'cse:requests'
DUPEFILTER_KEY = 'cse:dupefilter'


def clear_stats():
    server = redis.Redis(REDIS_HOST, REDIS_PORT)
    server.delete(STATS_KEY)
    server.delete(REQUESRTS_KEY)
    server.delete(DUPEFILTER_KEY)


if __name__ == "__main__":
    clear_stats()
