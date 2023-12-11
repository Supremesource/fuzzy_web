import json
from scrapy import Spider
from scrapy.http import Request

from articlescrapers.items import ArticlescrapersItem


class UctovaniSpider(Spider):
    name = 'uctovani'

    headers = {
        'authority': 'www.uctovani.net',
        'accept': '*/*',
        'accept-language': 'en,es-ES;q=0.9,es;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.uctovani.net',
        'referer': 'https://www.uctovani.net/clanky.php',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    def start_requests(self):
        yield Request(
            method='POST',
            url='https://www.uctovani.net/include/load_clanky.php',
            body='from=0&category=vse',
            meta={
                'from': 0,
            },
            callback=self.parse,
            headers=self.headers,
        )

    def parse(self, response):
        from_ = response.meta.get('from', 0) 
        page = response.meta.get('page', 1)
        articles = response.css('article.preview')
        self.logger.info(f'Found {len(articles)} articles in page {page} from {from_}')
        for article in articles:
            article_href = article.css('h3 a::attr(href)').get()
            if article_href is not None:
                article_url = 'https://www.uctovani.net/' + article_href
                self.logger.info(f'Found article {article_url}')
                article_title = article.css('h3 a::text').get()
                article_date = article.css('p.date-info::text').get()
                if article_date is not None:
                    self.logger.info(f'Found date {article_date}')
                    article_date = article_date.replace(' ','').split('.')
                    article_date = article_date[2] + '-' + article_date[1] + '-' + article_date[0]
                yield Request(
                    article_url,
                    callback=self.parse_article,
                    meta={
                        'title': article_title,
                        'date': article_date,
                    },
                    dont_filter=True,
                )

        '''if articles:
            next_from = from_ + 12
            yield Request(
                method='POST',
                url='https://www.uctovani.net/include/load_clanky.php',
                body=f'from={next_from}&category=vse',
                meta={
                    'page': page + 1,
                    'from': next_from,
                },
                callback=self.parse,
                headers=self.headers,
                dont_filter=True,
            )'''
    
    def parse_article(self, response):
        content = response.css('article.article').get()
        article_title = response.meta.get('title', None)
        article_date = response.meta.get('date', None)

        item = ArticlescrapersItem()
        item['url'] = response.url
        item['title'] = article_title
        item['date'] = article_date
        item['content'] = content

        yield item
