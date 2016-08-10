# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from .. import items
import re
class DownphotoSpider(CrawlSpider):
    name = "downphoto"
    allowed_domains = ["bz1080p.com"]
    start_urls = ['http://bz1080p.com/']

    rules = (
        Rule(LinkExtractor(allow=(r'http://bz1080p.com/archives/\d{3,8}',)), callback='parse_photo_folder', follow=True),
        Rule(LinkExtractor(allow=(r'http://bz1080p.com/page/\d+', )), follow=True)
        # Rule(LinkExtractor(deny=(r'http://bz1080p.com/archives/tag/\S*',)), follow=False),
        # Rule(LinkExtractor(deny=(r'http://bz1080p.com/archives/category/\S*',)), follow=False),
        # Rule(LinkExtractor(deny=(r'http://bz1080p.com/archiv0p.com/\S*',)), follow=False),
        # Rule(LinkExtractor(deny=(r'http://bz1080p.com/search/\S*',)), follow=False),
        # Rule(LinkExtractor(deny=(r'[^<>].*bbs[^<>].*',)), follow=False),
        # Rule(LinkExtractor(deny=(r'[^<>].*php[^<>].*',)), follow=False)
    )

    def parse_photo_folder(self, response):
        print '---------------------------'+response.url+'---------------------------'
        item = items.ImageItem()
        photo_pattern = r'http://bz1080p.com/wp-content/uploads/\d{4}/\d{1,2}/bz1080p\.com_[^x]*(jpg|jpeg|png|bmp)'
        soup = BeautifulSoup(response.body.decode('utf-8'), 'html.parser')
        temp_urls = soup.findAll(name='a', attrs={'href': re.compile(photo_pattern)})
        item['image_urls'] = []
        for temp_url in temp_urls:
            item['image_urls'].append(temp_url['href'])
        item['name'] = soup.find(name='a', attrs={'href': response.url}).string
        yield item


