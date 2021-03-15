from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Faculty(models.Model):
	Name = models.CharField(max_length=30)
	Description = models.CharField(max_length=200)
	def __str__(self):
		return self.Name
class User(AbstractUser):
	Sex_choise = ((0,"Male"),(1,"Female"),(2,"Other"))
	code = models.CharField(max_length=12, null = True, blank = True)
	DOB = models.DateTimeField(blank = True, null = True)
	PhoneNumber = models.IntegerField(blank=True, null = True)
	Sex = models.IntegerField(blank=True, choices= Sex_choise, null = True)
	Faculty = models.ForeignKey(Faculty, default=None, on_delete=models.CASCADE, blank=True, null = True)
	def __str__(self):
		return self.username
class Term(models.Model):
	idTerm = models.AutoField(primary_key=True)
	NameTerm = models.CharField(max_length=30)
	Description = models.TextField()
	ClosureDate = models.DateTimeField()
	FinalClosureDate = models.DateTimeField() 
	def __str__(self):
		return self.NameTerm
class Contribute(models.Model):
	Name = models.CharField(max_length=20)
	Description = models.CharField(max_length=100)
	Date = models.DateTimeField(auto_now_add = True)
	TermID = models.ForeignKey(Term, default=None, on_delete=models.CASCADE, blank=True, null = True)
	Status = models.BooleanField()
	UserID = models.ForeignKey(User, default=None, on_delete=models.CASCADE, blank=True, null = True)
	Document = models.FileField()
	Readed = models.BooleanField(null= True, blank=True)
	def __str__(self):
		return self.Name
class Data(models.Model):
	Data = models.ImageField()
	ContributeID = models.ForeignKey(Contribute, default=None, on_delete=models.CASCADE, blank=True, null = True)
class Comment(models.Model):
	ContributeID = models.ForeignKey(Contribute, default=None, on_delete=models.CASCADE, blank=True, null = True)
	UserID = models.ForeignKey(User, default=None, on_delete=models.CASCADE, blank=True, null = True)
	Comment = models.TextField()
	DateComment = models.DateTimeField(auto_now_add = True)
