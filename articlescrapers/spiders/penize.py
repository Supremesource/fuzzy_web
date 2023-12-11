import json
from scrapy import Spider
from scrapy.http import Request

from articlescrapers.items import ArticlescrapersItem


class PenizeSpider(Spider):
    name = 'penize'
    start_urls = [
        'https://www.penize.cz/clanky',
    ]

    def parse(self, response):
        page = response.meta.get('page', 1)
        articles = response.css('div#articleList div.article')
        self.logger.info(f'Found {len(articles)} articles in page {page}')

        for article in articles:
            article_href = article.css('h2 a::attr(href)').get()
            if article_href is not None:
                article_url = 'https:' + article_href
                yield Request(
                    article_url,
                    callback=self.parse_article,
                )

        '''next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield Request(
                response.urljoin(next_page),
                callback=self.parse,
                meta={'page': page + 1},
            )'''
    
    def parse_article(self, response):
        script = response.css('div#left > script::text').get()
        if script is not None:
            item = ArticlescrapersItem()
            article_data = json.loads(script, strict=False)
            article_date = article_data['datePublished'].split('T')[0]
            article_title = article_data['headline']
            article_content = '<div>' + ''.join(response.css('div#article_content > p').getall()) + '</div>'

            item['url'] = response.url
            item['title'] = article_title
            item['date'] = article_date
            item['content'] = article_content

            yield item
