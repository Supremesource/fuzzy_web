# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import datetime
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import asyncio
from itemadapter import ItemAdapter
from articles.models import Article

class ArticlescrapersPipeline:
    def process_item(self, item, spider):
        article = Article.objects.filter(url=item['url'], website=spider.name).first()
        if article:
            article.updated_at = datetime.datetime.now()
            article.is_last_run = True
            article.save()
        else:
            article = Article(
                website=spider.name,
                url=item['url'],
                title=item['title'],
                date=item['date'],
                content=item['content'],
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
                is_last_run=True
            )

        article.save()
        return item
