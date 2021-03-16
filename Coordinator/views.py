from django.shortcuts import render
from django.db import connection
from datetime import datetime
from Login.models import Contribute, Data, Comment
from django.http import HttpResponse

def getAuthGroup(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT auth_group.name FROM auth_group INNER JOIN login_user_groups ON auth_group.id = login_user_groups.group_id INNER JOIN login_user ON login_user.id = login_user_groups.user_id WHERE login_user.id = '%s'" ,
            [UserID]
        )
        auth_group = cursor.fetchall()[0][0]
    return auth_group
def daytime(Enddate):
    Begindate = datetime.today()
    Days_remaining = Enddate - Begindate
    return Days_remaining
def indexCoordinator(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Coordinator":
        with connection.cursor() as cursor:
            cursor.execute(
            "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm"
            )
            views = cursor.fetchall()
        Date = []
        for i in range(len(views)):
           Date.append(str(views[i][7]) +"/"+ str(daytime(views[i][3])))

        viewCoordinator = {'views': views, 'DateS': Date}
        return render(request, 'indexCoordinator.html', viewCoordinator)
    else:
        return render(request, 'login.html')


def viewContribute(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Coordinator":
        Contributes = Contribute.objects.filter(id=id)
        img = Data.objects.filter(ContributeID_id=id)
        dataContribute = {'Contributes': Contributes, 'img':img}
        return render(request, 'viewContribute.html', dataContribute)
    else:
        return render(request, 'login.html')
def sendMessenger(request, id, messenger):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Coordinator":
        Comment.objects.create(UserID_id = request.user.id, ContributeID_id = id, Comment = messenger)
        return render(request, 'viewContribute.html')
    else:
        return render(request, 'login.html')
def getMessenger(request, id):
    comment = Comment.objects.filter(ContributeID_id = id)
    html = []
    for i in comment:
        if getAuthGroup(i.UserID_id) == "Coordinator":
            html.append("<span class='you first'>"+i.Comment+" <span class='time'>"+i.DateComment.strftime("%m/%d/%y, %H:%M:%S")+"</span></span>")
        if getAuthGroup(i.UserID_id) == "Student":
            html.append("<span class='friend last'>"+i.Comment+"<span class='time'>"+i.DateComment.strftime("%m/%d/%y, %H:%M:%S")+"</span></span>")
    response = HttpResponse()
    response.writelines(html)
    return response
def public(request, status, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Coordinator":
        Contribute.objects.filter(id = id).update(Status = status)
        Contributes = Contribute.objects.filter(id=id)
        img = Data.objects.filter(ContributeID_id=id)
        dataContribute = {'Contributes': Contributes, 'img':img}
        return render(request, 'viewContribute.html', dataContribute)
    else:
        return render(request, 'login.html')
def filter(request, status, date_upload, read):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Coordinator":
        Status = Contribute.objects.filter(Status= status)
        Date = Contribute.objects.filter(Date= date_upload)
        Read = Contribute.objects.filter(Readed= read)
        Filters = {'Status': Status, 'Date': Date, 'Read': Read}
        return render(request, 'indexCoordinator.html', Filters)
    else:
        return render(request, 'login.html')