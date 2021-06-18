#####library.model.py
from django.db import models

# Create your models here.
class Books(models.Model):
	id = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=30)
	position = models.IntegerField()
	state = 1

class Authors(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=30)

class Subjects(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=30)

class Libcards(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=30)
	age = models.IntegerField()
	address = models.CharField(max_length=100)
	classoom = models.CharField(max_length=15)

class Borrowcards(models.Model):
	bookid = models.IntegerField()
	libcardid = models.IntegerField()
	borrow_date = models.DateField(auto_now=True)
	due_date = models.DateField()
	return_date = 'NULL'

class CardDetail(models.Model):
	BORROWCARD_ID = models.IntegerField()
	NAME = models.CharField(max_length=30)
	TITLE = models.CharField(max_length=30)
	DUE_DATE = models.DateField()
	RETURN_DATE = models.DateField()

class BookDetail(models.Model):
	BOOK_ID = models.IntegerField()
	TITLE = models.CharField(max_length=30)
	NAME = models.CharField(max_length=30)
	POSITION = models.CharField(max_length=10)


