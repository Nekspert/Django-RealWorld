from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True, verbose_name='E-mail')

    def __str__(self):
        return self.username
