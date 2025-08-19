from django.db import models


class Profile(models.Model):
    user = models.OneToOneField('myauth.User', on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.URLField(blank=True, null=True, verbose_name='Изображение')

    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        self.follows.add(profile)

    def unfollow(self, profile):
        self.follows.remove(profile)

    def is_following(self, profile) -> bool:
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile) -> bool:
        return self.followed_by.filter(pk=profile.pk).exists()
