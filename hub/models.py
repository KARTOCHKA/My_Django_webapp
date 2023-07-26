from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100, blank=True, null=True)

