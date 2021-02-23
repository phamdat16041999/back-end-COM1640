from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Faculty(models.Model):
	Name = models.CharField(max_length=30)
	Description = models.CharField(max_length=200)
	ClosureDate = models.DateTimeField()
	FinalClosureDate = models.DateTimeField()
	def __str__(self):
		return self.Name
class User(AbstractUser):
	Sex_choise = ((0,"Male"),(1,"Female"),(2,"Other"))
	code = models.CharField(max_length=12, null = True, blank = True)
	DOB = models.DateTimeField(blank = True, null = True)
	PhoneNumber = models.IntegerField(blank=True, null = True)
	Sex = models.IntegerField(blank=True, choices= Sex_choise, null = True)
	Faculty = models.ForeignKey(Faculty, default=None, on_delete=models.CASCADE, blank=True, null = True)


   
