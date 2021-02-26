from django.shortcuts import render
from django.http import HttpRequest
# Create your views here.
def indexStudent(request):
	return render(request, 'idexStudent.html')