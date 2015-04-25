#!/usr/bin/python
#-*-coding:utf-8-*-
import base64
import hashlib

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from cse.items import CseCrawlerItem
from cse.utils.select_result import clean_url
from cse.utils.compress_hash import compress_hash


class CseSpider(BaseSpider):
    name = "cse"

    #  allowed_hosts = ["njtech.edu.cn","127.0.0.1"]

    allowed_domains = ["cqt.njtech.edu.cn", "green.njut.asia"]

    # allowed_domains = ["njtech.edu.cn", "green.njut.asia"]
    # disallowed_domains = ["bbs.njtech.edu.cn", "online.njtech.edu.cn", "moodle.njtech.edu.cn"]

    start_urls = (
        'http://cqt.njtech.edu.cn/',
    )
    # start_urls = (
    #     'http://green.njtech.edu.cn/njut.html',
    # )

    # rules = (
    #     Rule(LinkExtractor(allow=r".*njtech.edu.cn.*"), ),
    # )
    # rules = (Rule(SgmlLinkExtractor(allow=('.*'), deny=(
    # '\.pdf', '\.zip', '\.rar', '\.doc', '\.docx', '\.ppt', '\.pptx', '\.xls', '\.xlsx')), callback='parse',
    #               follow=True, ), )

    def parse(self, response):
        response_selector = HtmlXPathSelector(text=response.body)

        all_url_list = response_selector.xpath('//a/@href').extract()

        encoding = response.encoding

        for next_link in all_url_list:
            next_link = clean_url(response.url, next_link, response.encoding)
            yield Request(url=next_link, callback=self.parse)

        cse_item = CseCrawlerItem()
        cse_item['url_id'] = compress_hash(hashlib.sha256(response.url.lower()).hexdigest())
        cse_item['url'] = response.url
        cse_item['content_type'] = response.headers.get('Content-Type', '')
        cse_item['content'] = response.body.decode(encoding, 'ignore').encode('utf-8')
        cse_item['encoding'] = encoding

        yield cse_item



