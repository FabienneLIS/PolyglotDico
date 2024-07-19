from django.db import models

# Create your models here.
class listingWord(models.Model):
    nameList = models.CharField(max_length=100)
    theme = models.CharField(max_length=80)
