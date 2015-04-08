import re

__author__ = 'TianShuo'

from scrapy import signals
from scrapy.http import Request
from scrapy.utils.httpobj import urlparse_cached
from scrapy import log


class NjtechOffsiteMiddleware(object):
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def process_spider_output(self, response, result, spider):
        for x in result:
            if isinstance(x, Request):
                if x.dont_filter or self.should_follow(x, spider):
                    yield x
                else:
                    domain = urlparse_cached(x).hostname
                    if domain and domain not in self.domains_seen:
                        self.domains_seen.add(domain)
                        log.msg(format="Filtered offsite request to %(domain)r: %(request)s",
                                level=log.INFO, spider=spider, domain=domain, request=x)
                        self.stats.inc_value('offsite/domains', spider=spider)
                    self.stats.inc_value('offsite/filtered', spider=spider)
            else:
                yield x

    def should_follow(self, request, spider):
        allowed_regex = self.host_allowed_regex
        disallowed_regex = self.host_disallowed_regex
        # hostname can be None for wrong urls (like javascript links)
        host = urlparse_cached(request).hostname or ''

        allowed_res = bool(allowed_regex.search(host))
        disallowed_res = not bool(disallowed_regex.search(host))
        return allowed_res and disallowed_res

    def get_allowed_host_regex(self, spider):
        """Override this method to implement a different offsite policy"""
        allowed_domains = getattr(spider, 'allowed_domains', None)
        if not allowed_domains:
            return re.compile('')  # allowed all by default
        regex = r'^(.*\.)?(%s)$' % '|'.join(re.escape(d) for d in allowed_domains if d is not None)
        return re.compile(regex)

    def get_disallowed_host_regex(self, spider):
        """Override this method to implement a different offsite policy"""
        disallowed_domains = getattr(spider, 'disallowed_domains', None)
        if not disallowed_domains:
            return re.compile('12345679')  # no domain is fucking like this
        regex = r'^(.*\.)?(%s)$' % '|'.join(re.escape(d) for d in disallowed_domains if d is not None)
        return re.compile(regex)

    def spider_opened(self, spider):
        self.host_allowed_regex = self.get_allowed_host_regex(spider)
        self.host_disallowed_regex = self.get_disallowed_host_regex(spider)
        self.domains_seen = set()
