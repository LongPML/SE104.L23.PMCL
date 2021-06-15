from django.db import models

# Create your models here.
class Book(models.Model):
        title = models.TextField()
        author = models.TextField(default=" ")
        topic = models.TextField(default=' ')
        posision = models.TextField(default=' ')