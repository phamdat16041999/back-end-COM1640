from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Faculty(models.Model):
	Name = models.CharField(max_length=30)
	Description = models.CharField(max_length=200)
	def __str__(self):
		return self.Name

class Term(models.Model):
	idTerm = models.AutoField(primary_key=True)
	NameTerm = models.CharField(max_length=30)
	Description = models.TextField()
	ClosureDate = models.DateTimeField()
	FinalClosureDate = models.DateTimeField()
class User(AbstractUser):
	Sex_choise = ((0,"Male"),(1,"Female"),(2,"Other"))
	code = models.CharField(max_length=12, null = True, blank = True)
	DOB = models.DateTimeField(blank = True, null = True)
	PhoneNumber = models.IntegerField(blank=True, null = True)
	Sex = models.IntegerField(blank=True, choices= Sex_choise, null = True)
	Faculty = models.ForeignKey(Faculty, default=None, on_delete=models.CASCADE, blank=True, null = True)
class Term(models.Model):
	idTerm = models.AutoField(primary_key=True)
	NameTerm = models.CharField(max_length=30)
	Description = models.TextField()
	ClosureDate = models.DateTimeField()
	FinalClosureDate = models.DateTimeField()
class Contribute(models.Model):
	NameContribute = models.CharField(max_length=20)
	DateContribute = models.DateTimeField()
	Term = models.ForeignKey(Term, default=None, on_delete=models.CASCADE, blank=True, null = True)
	Status = models.TextField()
	User = models.ForeignKey(User, default=None, on_delete=models.CASCADE, blank=True, null = True)
	Image = models.ImageField()

class Data(models.Model):
	idData = models.AutoField(primary_key=True)
	Data = models.FileField()
	Contribute = models.ForeignKey(Contribute, default=None, on_delete=models.CASCADE, blank=True, null = True)

class Comment(models.Model):
	Contribute = models.ForeignKey(Contribute, default=None, on_delete=models.CASCADE, blank=True, null = True)
	User = models.ForeignKey(User, default=None, on_delete=models.CASCADE, blank=True, null = True)
	Comment = models.TextField()
	DateComment = models.DateTimeField()