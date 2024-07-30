# models.py
from django.db import models


class Dictionary(models.Model):
    name = models.CharField(max_length=100)
    # autres champs si nécessaire

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Word(models.Model):
    source_word = models.CharField(max_length=100)
    target_word = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
