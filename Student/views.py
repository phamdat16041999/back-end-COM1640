from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.db import connection
from Login.models import Contribute, Term, Data, Comment
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
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
    Contributes = {'Contributes': Contribute.objects.filter(UserID_id=request.user.id).order_by('-Date')}
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
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT login_contribute.Document, login_contribute.Name, login_contribute.Description FROM ((login_contribute INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm) INNER JOIN login_user ON login_contribute.UserID_id = login_user.id) WHERE login_term.idTerm = '%s' and login_user.id ='%s'" ,
            [id,request.user.id]
        )
        Data = cursor.fetchall()
    if len(Data) > 0:
        return redirect('/Student/ViewDeadline/viewUpdate/'+str(id))
    else:
        ternID = {'ternID':id}
        return render(request, 'uploadFile.html', ternID)
def viewUpdate(request,id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT login_contribute.Document, login_contribute.Name, login_contribute.Description FROM ((login_contribute INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm) INNER JOIN login_user ON login_contribute.UserID_id = login_user.id) WHERE login_term.idTerm = '%s' and login_user.id ='%s'" ,
            [id,request.user.id]
        )
        DataNoImage = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT login_data.Data FROM (((login_contribute INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm) INNER JOIN login_user ON login_contribute.UserID_id = login_user.id) INNER JOIN login_data ON login_contribute.id = login_data.ContributeID_id) WHERE login_term.idTerm = '%s' and login_user.id ='%s' ",
            [id,request.user.id]
        )
        DataImage = cursor.fetchall()
    ternID = {'ternID':id, 'DataNoImage': DataNoImage,'DataImage': DataImage}
    return render(request, 'Update.html', ternID)
def viewUploaded(request,id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT login_contribute.Document, login_contribute.Name, login_contribute.Description FROM ((login_contribute INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm) INNER JOIN login_user ON login_contribute.UserID_id = login_user.id) WHERE login_term.idTerm = '%s' and login_user.id ='%s'" ,
            [id,request.user.id]
        )
        DataNoImage = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT login_data.Data FROM (((login_contribute INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm) INNER JOIN login_user ON login_contribute.UserID_id = login_user.id) INNER JOIN login_data ON login_contribute.id = login_data.ContributeID_id) WHERE login_term.idTerm = '%s' and login_user.id ='%s' ",
            [id,request.user.id]
        )
        DataImage = cursor.fetchall()
    return render(request, 'viewUploaded.html', {'DataNoImage': DataNoImage,'DataImage': DataImage})
def uploadContribute(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.FILES['contribute'] and request.FILES['image1'] and request.FILES['image2']:
            nameContribute = request.POST.get('nameContribute','')
            description = request.POST.get('description','')
            contribute = request.FILES['contribute']
            image1 = request.FILES['image1']
            image2 = request.FILES['image2']
            Contribute.objects.create(Name = nameContribute, Description = description, TermID_id = id, Status = False, UserID_id = request.user.id, Document = contribute)
            Data.objects.create(Data = image1, ContributeID_id = Contribute.objects.latest('id').id)
            Data.objects.create(Data = image2, ContributeID_id = Contribute.objects.latest('id').id)
            # Contribute.objects.create()
            return redirect('/')
        else:
            # Not found 404
            return redirect('/')
    else:
        return render(request, 'login.html')
def sendMessenger(request, id, messenger):
    ContributeID = Contribute.objects.get(TermID = id, UserID = request.user.id)
    Comment.objects.create(UserID_id = request.user.id, ContributeID_id = ContributeID.id, Comment = messenger)
    ternID = {'ternID':id}
    return render(request, 'Update.html', ternID)
def getMessenger(request, id):
    ContributeID = Contribute.objects.get(TermID = id, UserID = request.user.id)
    comment = Comment.objects.filter(ContributeID_id = ContributeID.id)
    html = []
    for i in comment:
        if getAuthGroup(i.UserID_id) == "Student":
            html.append("<span class='you first'>"+i.Comment+"</span>")
        if getAuthGroup(i.UserID_id) == "Coordinator":
            html.append("<span class='friend last'>"+i.Comment+"</span>")
    response = HttpResponse()
    response.writelines(html)
    return response
def Update(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.FILES['contribute'] and request.FILES['image1'] and request.FILES['image2']:
            nameContribute = request.POST.get('nameContribute','')
            description = request.POST.get('description','')
            contribute = request.FILES['contribute']
            image1 = request.FILES['image1']
            image2 = request.FILES['image2']
            Contribute.objects.filter(TermID_id = id,UserID_id = request.user.id).delete()
            Contribute.objects.create(Name = nameContribute, Description = description, TermID_id = id, Status = False, UserID_id = request.user.id, Document = contribute)
            Data.objects.create(Data = image1, ContributeID_id = Contribute.objects.latest('id').id)
            Data.objects.create(Data = image2, ContributeID_id = Contribute.objects.latest('id').id)
            # Contribute.objects.create()
            return redirect('/Student/ViewDeadline/viewUpdate/'+str(id))
        else:
            # Not found 404
            return redirect('/')
    else:
        return render(request, 'login.html')


