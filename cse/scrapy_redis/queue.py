#!/usr/bin/python
#-*-coding:utf-8-*-
import json
import redis

from scrapy.utils.reqser import request_to_dict, request_from_dict


# default values
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_HOST_Notify = 'localhost'
REDIS_PORT_Notify = 6379

try:
    import cPickle as pickle
except ImportError:
    import pickle


class Base(object):
    """Per-spider queue/stack base class"""

    def __init__(self, server, spider, key):
        """Initialize per-spider redis queue.

        Parameters:
            server -- redis connection
            spider -- spider instance
            key -- key for this queue (e.g. "%(spider)s:queue")
        """
        self.server = server
        self.spider = spider
        self.key = key % {'spider': spider.name}

    def _encode_request(self, request):
        """Encode a request object"""
        return pickle.dumps(request_to_dict(request, self.spider), protocol=-1)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        return request_from_dict(pickle.loads(encoded_request), self.spider)

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, request):
        """Push a request"""
        raise NotImplementedError

    def pop(self):
        """Pop a request"""
        raise NotImplementedError

    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)


class SpiderQueue(Base):
    def __len__(self):
        """Return the length of the queue"""
        return self.server.llen(self.key)

    def push(self, request):
        """Push a request"""
        self.server.lpush(self.key, self._encode_request(request))

    def pop(self):
        """Pop a request"""
        data = self.server.rpop(self.key)
        if data:
            return self._decode_request(data)


class SpiderPriorityQueue(Base):
    """Per-spider priority queue abstraction using redis' sorted set"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.zcard(self.key)

    def push(self, request):
        """Push a request"""
        data = self._encode_request(request)
        pairs = {data: -request.priority}
        self.server.zadd(self.key, **pairs)

    def pop(self):
        """Pop a request"""
        # use atomic range/remove using multi/exec
        pipe = self.server.pipeline()
        pipe.multi()
        pipe.zrange(self.key, 0, 0).zremrangebyrank(self.key, 0, 0)
        results, count = pipe.execute()
        if results:
            return self._decode_request(results[0])


class SpiderStack(Base):
    """Per-spider stack"""

    def __len__(self):
        """Return the length of the stack"""
        return self.server.llen(self.key)

    def push(self, request):
        """Push a request"""
        self.server.lpush(self.key, self._encode_request(request))

    def pop(self):
        """Pop a request"""
        data = self.server.lpop(self.key)
        if data:
            return self._decode_request(data)


class RedisKV(object):
    def __init__(self, server, port):
        self.server = redis.Redis(server, port)

    @classmethod
    def from_settings(cls, settings):
        server = settings.get('REDIS_HOST', REDIS_HOST)
        port = settings.get('REDIS_PORT', REDIS_PORT)

        return cls(server, port)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls.from_settings(settings)

    def set(self, key, value):
        self.server.set(key, value)

    def get(self, key):
        return self.server.get(key)

    def exists(self, key):
        return self.server.exists(key)


class IndexNotifyQueue(object):

    def __init__(self, server, port, key):
        self.server = redis.Redis(server, port)
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        server = settings.get('REDIS_HOST_Notify', REDIS_HOST_Notify)
        port = settings.get('REDIS_PORT_Notify', REDIS_PORT_Notify)
        key = settings.get('IndexNotifyQueue', 'IndexNotifyQueue')
        return cls(server, port, key)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls.from_settings(settings)

    def __len__(self):
        """Return the length of the queue"""
        return self.server.llen(self.key)

    def _encode_index_notify(self, index_notify):
        """Encode a request object"""
        return json.dumps(index_notify)

    def _decode_index_notify(self, index_notify):
        """Decode an request previously encoded"""
        return json.loads(index_notify)

    def push(self, index_notify):
        """Push a request"""
        self.server.lpush(self.key, self._encode_index_notify(index_notify))

    def pop(self):
        """Pop a request"""
        data = self.server.rpop(self.key)
        if data:
            return self._decode_index_notify(data)


__all__ = ['RedisKV', 'IndexNotifyQueue', 'SpiderQueue', 'SpiderPriorityQueue', 'SpiderStack']
