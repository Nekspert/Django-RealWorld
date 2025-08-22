from django.db import models

from core.models import TimestampModel


class Comment(TimestampModel):
    body = models.TextField()
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.author.user.username + ' : ' + self.article.title[:25]
