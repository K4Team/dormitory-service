from django.db import models


# Create your models here.

class User(models.Model):
    id = models.CharField(primary_key=True, null=False, max_length=20)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    email = models.CharField(max_length=255)
    income = models.CharField(max_length=20)
    create_date = models.DateTimeField()
