from django.db import models

from core.models import TimestampModel


class Tag(TimestampModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.tag
