from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email