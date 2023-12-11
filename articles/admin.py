from django.contrib import admin
from django.utils.html import format_html

from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['website', 'title', 'ratio', 'partial_ratio', 'token_sort_ratio', 'token_set_ratio']
    list_filter = ['website', 'is_last_run']
    list_per_page = 20
    list_display_links = ['title']


admin.site.register(Article, ArticleAdmin)