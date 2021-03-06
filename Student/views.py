from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.db import connection
from Login.models import Contribute, Term, Data
from datetime import datetime
from .forms import DataForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
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

def book_list(request):
    book_list = Data.objects.all()
    return render(request, 'book_list.html',{
        'books': book_list
        })

def UploadFile(request,id):
    if request.method == 'POST':

        form = DataForm(request.POST, request.FILES )
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            return redirect('book_list')
            # return render(request, 'book_list.html')
    else:
        form = DataForm()
    return render(request, 'upload_book.html',{
        'form': form
        })
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile'] and request.FILES['myfile1'] :
        myfile = request.FILES['myfile']
        myfile1 = request.FILES['myfile1']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        filename = fs.save(myfile1.name, myfile1)
        uploaded_file_url = fs.url(filename)
        return render(request, 'ViewDeadline.html')
    return render(request, 'simple_upload.html')
    # uploaded_file_url = fs.url(filename)
    #     return render(request, 'core/simple_upload.html', {
    #         'uploaded_file_url': uploaded_file_url
    #     })