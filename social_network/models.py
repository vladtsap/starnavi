from django.contrib.auth.models import AbstractUser
from django.db import models


class SocialUser(AbstractUser):
    last_activity = models.DateTimeField(auto_now=True)
