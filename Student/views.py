from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.db import connection
from Login.models import Contribute, Term, Data
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
# Create your views here.
def getAuthGroup(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT auth_group.name FROM auth_group INNER JOIN login_user_groups ON auth_group.id = login_user_groups.group_id INNER JOIN login_user ON login_user.id = login_user_groups.user_id WHERE login_user.id = '%s'" ,
            [UserID]
        )
        auth_group = cursor.fetchall()[0][0]
    return auth_group
def indexStudent(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Student":
        return render(request, 'indexStudent.html')
    else:
        return render(request, 'login.html')
def ViewContributes(request):
   Contributes = {'Contributes': Contribute.objects.filter(User=request.user.id).order_by('-DateContribute')}
   return render(request, 'MyContribute.html', Contributes)
def ViewDeadline(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT DISTINCT YEAR(ClosureDate) FROM login_term as year"
        )
        year = cursor.fetchall()
    Year = []
    for i in range(len(year)):
        Year.append(year[i][0])
        Year.sort(reverse=True)
    ViewDeadlines = {'ViewDeadlines': Term.objects.all().order_by('-ClosureDate'), 'Now': datetime.now(), 'Year': Year}
    return render(request, 'ViewDeadline.html', ViewDeadlines)
def ViewDeadlineYear(request, id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT DISTINCT YEAR(ClosureDate) FROM login_term as year"
        )
        year = cursor.fetchall()
    Year = []
    for i in range(len(year)):
        Year.append(year[i][0])
        Year.sort(reverse=True)
    ViewDeadlines = {'ViewDeadlines': Term.objects.all().order_by('-ClosureDate'), 'id': str(id), 'Now': datetime.now(), 'Year': Year}
    return render(request, 'ViewDeadlineYear.html', ViewDeadlines)
def viewUpload(request,id):
    ternID = {'ternID':id}
    return render(request, 'uploadFile.html', ternID)
def uploadContribute(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.FILES['contribute'] and request.FILES['image1'] and request.FILES['image2']:
            nameContribute = request.POST.get('nameContribute','')
            description = request.POST.get('description','')
            contribute = request.FILES['contribute']
            image1 = request.FILES['image1']
            image2 = request.FILES['image2']
            fs = FileSystemStorage()
            filename = fs.save(contribute.name, contribute)
            filename = fs.save(image1.name, image1)
            filename = fs.save(image2.name, image2)
            Contribute.objects.create(Name = nameContribute, Description = description, TermID_id = id, Status = False, UserID_id = request.user.id, Document = contribute.name)
            Data.objects.create(Data = image1.name, ContributeID_id = Contribute.objects.latest('id').id)
            Data.objects.create(Data = image2.name, ContributeID_id = Contribute.objects.latest('id').id)
            uploaded_file_url = fs.url(filename)
            # Contribute.objects.create()
            return redirect('/')
        else:
            # Not found 404
            return redirect('/')
    else:
        return render(request, 'login.html')

