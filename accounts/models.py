from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    phone = models.CharField(max_length=20,
                             blank=True,
                             verbose_name="telefone")

    def __str__(self):
        return self.get_full_name() or self.username

