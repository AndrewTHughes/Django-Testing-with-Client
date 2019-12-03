from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    username = models.CharField(max_length=20, primary_key=True)
    friends = models.ManyToManyField("self")
