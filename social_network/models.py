from django.contrib.auth.models import AbstractUser
from django.db import models


class SocialUser(AbstractUser):
    last_activity = models.DateTimeField(auto_now=True)


class Post(models.Model):
    author = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField(SocialUser, through='Like', related_name='liked_posts')


class Like(models.Model):
    user = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    made_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
