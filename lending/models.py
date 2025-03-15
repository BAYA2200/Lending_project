from django.db import models

# Create your models here.

from django.db import models


class AdminSettings(models.Model):
    manager_email = models.EmailField("Email менеджера", unique=True)

    def __str__(self):
        return self.manager_email

    class Meta:
        verbose_name = "Настройки менеджера"
        verbose_name_plural = "Настройки менеджера"
