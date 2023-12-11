from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from articlescrapers.spiders.mesec import MesecSpider
from articlescrapers.spiders.penize import PenizeSpider
from articlescrapers.spiders.uctovani import UctovaniSpider
from articlescrapers.spiders.podnikatel import PodnikatelSpider
from articlescrapers.spiders.businessinfo import BusinessinfoSpider

from articles.models import Article

class Command(BaseCommand):
  help = "Release the spiders"

  def handle(self, *args, **options):
    # set last run to false for all articles
    Article.objects.all().update(is_last_run=False)
    
    process = CrawlerProcess(get_project_settings())
    process.crawl(UctovaniSpider)
    process.crawl(PenizeSpider)
    process.crawl(MesecSpider)
    process.crawl(PodnikatelSpider)
    process.crawl(BusinessinfoSpider)
    process.start()

    # delete all articles that are not from last run
    Article.objects.filter(is_last_run=False).delete()

    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process

    articles = Article.objects.filter(is_last_run=True)
    # compare each article with each other
    for article in articles:
        number_of_articles = 0
        ratio = 0
        partial_ratio = 0
        token_sort_ratio = 0
        token_set_ratio = 0
        # exclude current article from comparison
        articles_exclude_current = articles.exclude(id=article.id)
        for other_article in articles_exclude_current:
            number_of_articles += 1
            ratio += fuzz.ratio(article.title, other_article.title)
            partial_ratio += fuzz.partial_ratio(article.title, other_article.title)
            token_sort_ratio += fuzz.token_sort_ratio(article.title, other_article.title)
            token_set_ratio += fuzz.token_set_ratio(article.title, other_article.title)
        
        # get average of all ratios
        article.ratio = ratio / number_of_articles
        article.partial_ratio = partial_ratio / number_of_articles
        article.token_sort_ratio = token_sort_ratio / number_of_articles
        article.token_set_ratio = token_set_ratio / number_of_articles
        article.save()

      
      




