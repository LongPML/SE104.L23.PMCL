#####library.model.py
from django.db import models

# Create your models here.
class Books(models.Model):
	title = models.CharField(max_length=30)
	position = models.IntegerField()
	state = 1

class Authors(models.Model):
	name = models.CharField(max_length=30)

class Subjects(models.Model):
	name = models.CharField(max_length=30)

class Authors_Books(models.Model):
	authorid = models.CharField(max_length=10)
	bookid = models.CharField(max_length=10)

class Subjects_Books(models.Model):
	subjectid = models.CharField(max_length=10)
	bookid = models.CharField(max_length=10)