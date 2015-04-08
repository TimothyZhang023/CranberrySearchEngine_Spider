#!/usr/bin/python
#-*-coding:utf-8-*-

from scrapy import log


class SaveHtmlPipeline(object):
    def process_item(self, item, spider):
        print ("save:" + item['url'] + " encode:" + item['encoding']  )

        filename = 'html/' + item['url_id'] + '.html'
        open(filename, 'wb').write(item['content'])

        return item

    def handle_error(self, e):
        log.err(e)

