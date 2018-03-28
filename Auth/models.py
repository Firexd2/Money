from django.db import models
from django.contrib.auth.models import AbstractUser
from Core.models import Settings


class User(AbstractUser):
    settings = models.OneToOneField(Settings, on_delete=models.CASCADE, blank=True, null=True)
    first_log_in = models.BooleanField(default=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.username


class VisitationIp(models.Model):
    ip = models.GenericIPAddressField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return 'IP: %s' % self.ip

    class Meta:
        verbose_name = 'Ip адрес'
        verbose_name_plural = 'Ip адреса'
