import json
from datetime import datetime
from scrapy import Spider
from scrapy.http import Request

from articlescrapers.items import ArticlescrapersItem
from articles.models import Article

class BusinessinfoSpider(Spider):
    name = 'businessinfo'
    start_urls = [
        'https://www.businessinfo.cz/clanky/?pg=1-1&ajax=1',
    ]

    def parse(self, response):
        page = response.meta.get('page', 1)
        data = json.loads(response.body)
        articles = data['posts']
        self.logger.info(f'Found {len(articles)} posts in page {page}')
        for article in articles:
            article_url = article['link']
            article_title = article['name']
            article_date = article.get('meta',{}).get('date')
            if article_date is not None:
                article_date = article_date.split('.')
                article_date = article_date[2] + '-' + article_date[1] + '-' + article_date[0]
            
            yield Request(
                article_url,
                callback=self.parse_article,
                meta={'title': article_title, 'date': article_date},
            )

        '''show_more_button_href = data.get('show_more_button')
        if show_more_button_href is not None:
            next_url = 'https://www.businessinfo.cz/clanky/?pg={page}-{page}&ajax=1'.format(page=page+1)
            yield Request(
                next_url,
                callback=self.parse,
                meta={'page': page + 1},
            )'''
    
    def parse_article(self, response):
        script = response.css('script.yoast-schema-graph::text').get()
        if script is not None:
            data = json.loads(script, strict=False)
            item = ArticlescrapersItem()
            article_url = response.url
            article_title = response.meta.get('title')
            article_date = response.meta.get('date')
            article_content = response.css('section.article-content').get()
            item['url'] = article_url
            item['title'] = article_title
            item['date'] = article_date
            item['content'] = article_content
            yield item
