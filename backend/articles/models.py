from django.db import models

from core.models import TimestampModel


class Article(TimestampModel):
    slug = models.SlugField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='articles')
    tags = models.ManyToManyField('tags.Tag', related_name='articles')

    def __str__(self):
        return self.title[:25]
