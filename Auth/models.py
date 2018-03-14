from django.db import models
from django.contrib.auth.models import AbstractUser
from Core.models import Settings


class User(AbstractUser):
    settings = models.OneToOneField(Settings, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(auto_now=True)
