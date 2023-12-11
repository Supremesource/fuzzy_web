from django.db import models


class Article(models.Model):
    website = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    url = models.URLField()
    date = models.DateField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_last_run = models.BooleanField(default=False)
    ratio = models.FloatField(default=0)
    partial_ratio = models.FloatField(default=0)
    token_sort_ratio = models.FloatField(default=0)
    token_set_ratio = models.FloatField(default=0)


    def __str__(self):
        return self.title
