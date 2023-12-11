import json
from scrapy import Spider
from scrapy.http import Request

from articlescrapers.items import ArticlescrapersItem


class MesecSpider(Spider):
    name = 'mesec'
    start_urls = [
        'https://www.mesec.cz/clanky/#clanek-21',
    ]

    def parse(self, response):
        page = response.meta.get('page', 1)
        articles = response.css('div.design-box__content li.design-list__item')
        self.logger.info(f'Found {len(articles)} articles in page {page}')

        for article in articles:
            article_href = article.css('a.design-article__link--default::attr(href)').get()
            if article_href is not None:
                article_url = 'https://www.mesec.cz' + article_href
                article_title = article.css('h3.element-heading-reset::text').get()
                self.logger.info(f'Found article {article_url}')
                
                yield Request(
                    article_url,
                    callback=self.parse_article,
                    meta={'title': article_title},
                )


        '''next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield Request(
                response.urljoin(next_page),
                callback=self.parse,
                meta={'page': page + 1},
            )'''
    
    def parse_article(self, response):
        script = response.xpath('//script[contains(text(), "mainEntityOfPage")]/text()').get()
        if script is not None:
            item = ArticlescrapersItem()
            article_data = json.loads(script, strict=False)
            article_date = article_data['datePublished'].split('T')[0]

            item['url'] = response.url
            item['title'] = response.meta.get('title')
            item['date'] = article_date
            item['content'] = response.css('div.js-sticker-compare-wrapper').get()

            yield item
