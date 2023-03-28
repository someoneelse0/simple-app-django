from django.db import models

# Create your models here.

class Clients(models.Model):
    username=models.CharField(max_length=30)
    keykey=models.CharField(max_length=30)
