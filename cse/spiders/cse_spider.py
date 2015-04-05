#!/usr/bin/python
#-*-coding:utf-8-*-
import hashlib

import time
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from cse.items import CseCrawlerItem
from cse.utils.select_result import clean_url
from tld import get_tld
from cse.scrapy_redis.queue import IndexNotifyQueue, RedisKV


class CseSpider(BaseSpider):
    name = "cse"

    #  allowed_hosts = ["njtech.edu.cn","127.0.0.1"]

    start_urls = (
        'http://127.0.0.1/0/njut.html',
    )

    # rules = (
    #     Rule(LinkExtractor(allow=r".*njtech.edu.cn.*"), ),
    # )
    # rules = (Rule(SgmlLinkExtractor(allow=('.*'), deny=(
    # '\.pdf', '\.zip', '\.rar', '\.doc', '\.docx', '\.ppt', '\.pptx', '\.xls', '\.xlsx')), callback='parse',
    #               follow=True, ), )

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

    def parse(self, response):
        # if not self.pass_item(response.url):
        #     return

        print ("now processing:" + response.url)
        #self.save_html(response)

        response_selector = HtmlXPathSelector(text=response.body)

        all_url_list = response_selector.xpath('//a/@href').extract()

        title = response_selector.xpath('//title/text()').extract()
        description = response_selector.xpath('//meta/@description').extract()
        keywords = response_selector.xpath('//meta/@keywords').extract()

        if len(title):
            title = title[0].strip()
        else:
            title = ''
        if len(description):
            description = description[0]
        else:
            description = ''

        if len(keywords):
            keywords = keywords[0]
        else:
            keywords = ''

        if all_url_list:
            #print all_url_list
            pass
        else:
            self.log(" no url found in" + response.url)

        for next_link in all_url_list:
            next_link = clean_url(response.url, next_link, response.encoding)

            if self.filter_item_by_domain(next_link):
                #self.log("next_link:" + next_link)
                #print "add into queue:" + next_link
                yield Request(url=next_link, callback=self.parse)
            else:
                #print("skip due to domain mismatch: " + next_link)
                pass

        cse_item = CseCrawlerItem()
        cse_item['redis_id'] = hashlib.sha256(response.url).hexdigest()
        cse_item['url'] = response.url
        cse_item['content_type'] = response.headers.get('Content-Type', '')
        cse_item['title'] = title
        cse_item['content'] = response.body
        cse_item['encoding'] = response.encoding
        cse_item['fetch_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        yield cse_item

    def save_html(self, response):

        content_type = response.headers.get('Content-Type', '')
        # if content_type not in self.HTML_FILE_CONTENT_TYPE:
        #     print 'skip ' + response.url + ' due to Content-Type'
        #     return

        hash_key = hashlib.sha256(response.url).hexdigest()
        self.log('Save_html:' + response.url + " Content-Type:" + content_type)

        filename = 'html/' + hash_key + '.html'
        open(filename, 'wb').write(response.body)

        index_notify = {'hash_key': hash_key, 'storage_type': 'local_fs', 'encoding': response.encoding}
        index_notify_queue = IndexNotifyQueue()
        index_notify_queue.push(index_notify)

    def filter_item_by_domain(self, next_link):
        try:
            if next_link:
                domain = get_tld(next_link)
                if domain in self.ALLOWED_DOMAIN:
                    return True
                return False
            else:
                return False
        except Exception, e:
            #print e
            return False


    def filter_item_by_key(self, next_link):
        """
        Return true means new url ,false represent old url
        """
        try:
            redis_kv = RedisKV()
            redis_id = hashlib.sha256(next_link).hexdigest() + "_item"
            if redis_kv.exists(redis_id):
                return False
            else:
                redis_kv.set(redis_id, 0)
                return True
        except Exception, e:
            print e
            return True

            #
            # def filter_item_by_content_type(self, url, content_type_text='text'):
            #     return True
            #     """
            #     Return true or false (1 or 0) based on HTTP Content-Type.
            #     Accepts either a url (string) or a "urllib.urlopen" file.
            #
            #     Defaults to 'text' type.
            #     Only looks at start of content-type, so you can be as vague or precise
            #     as you want.
            #     For example, 'image' will match 'image/gif' or 'image/jpg'.
            #     """
            #     hash_key = hashlib.sha256(url).hexdigest() + "_content_type"
            #     redis_kv = RedisKV()
            #
            #     if redis_kv.exists(hash_key):
            #         if redis_kv.get(hash_key).find(content_type_text) == 0:
            #             return True
            #         else:
            #             return False
            #     else:
            #         try:
            #             socket.setdefaulttimeout(2)
            #             url_r = urllib2.urlopen(url)
            #             content_type = url_r.info().getheader("Content-Type")
            #             redis_kv.set(hash_key, content_type)
            #             if content_type and content_type.find(content_type_text) == 0:
            #                 # print url, ' \'s Content-Type:', content_type
            #                 return True
            #             else:
            #                 return False
            #         except Exception, e:
            #             print e
            #             return False
