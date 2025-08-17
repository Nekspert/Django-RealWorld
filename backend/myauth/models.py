from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True, verbose_name='E-mail')
    bio = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.URLField(blank=True, null=True)
