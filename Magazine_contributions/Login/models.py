from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	Sex_choise = ((0,"Male"),(1,"Female"),(2,"Other"))
	code = models.CharField(max_length=12)
	DOB = models.DateTimeField()
	PhoneNumber = models.IntegerField(blank=True)
	Sex = models.IntegerField(blank=True, choices= Sex_choise)
class Faculty(models.Model):
	Name = models.CharField(max_length=30)
	Description = models.CharField(max_length=200)
	ClosureDate = models.DateTimeField()
	FinalClosureDate = models.DateTimeField()


   
