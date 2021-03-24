from django.shortcuts import render
from django.db import connection
from datetime import datetime
from Login.models import Contribute, Term, Data, Comment, User, Faculty
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
            "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [User.objects.filter(id= request.user.id)[0].Faculty_id]
            )
            views = cursor.fetchall()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT YEAR(ClosureDate) FROM login_term as year"
            )
            year = cursor.fetchall()
        Year = []
        for i in range(len(year)):
            Year.append(year[i][0])
        Date = []
        for i in range(len(views)):
           Date.append(str(views[i][7]) +"/"+ str(daytime(views[i][3])))
        viewCoordinator = {'views': views, 'DateS': Date, 'Year': Year}
        return render(request, 'indexCoordinator.html', viewCoordinator)
    else:
        return render(request, 'login.html')
def viewContribute(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Coordinator":
        Contributes = Contribute.objects.filter(id=id)
        Contribute.objects.filter(id=id).update(Readed = 1)
        print(Contributes)
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
        return render(request, 'indexCoordinator.html', dataContribute)
    else:
        return render(request, 'login.html')
def filter(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Coordinator":
        Status = request.POST.get('Status','')
        Year = request.POST.get('Year','')
        Read = request.POST.get('Read','')
        if Status == "Private":
            Status = 0
        if Status == "Public":
            Status = 1
        if Read == "Read":
            Read = 1
        if Read == "Unread":
            Read = 0
        if Status == 'All' and Year == 'All' and Read == 'All':
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [User.objects.filter(id= request.user.id)[0].Faculty_id]
                )
                views = cursor.fetchall()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT DISTINCT YEAR(ClosureDate) FROM login_term as year"
                )
                year = cursor.fetchall()
            Year = []
            for i in range(len(year)):
                Year.append(year[i][0])
            Date = []
            for i in range(len(views)):
                Date.append(str(views[i][7]) +"/"+ str(daytime(views[i][3])))
            viewCoordinator = {'views': views, 'DateS': Date, 'Year': Year}
            return render(request, 'indexCoordinator.html', viewCoordinator)
        if Status == 'All' and Year == 'All' and Read != 'All':
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE login_contribute.Readed = '%s' AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [Read, User.objects.filter(id= request.user.id)[0].Faculty_id]
                )
                views = cursor.fetchall()
            Date = []
            for i in range(len(views)):
                Date.append(str(views[i][7]) +"/"+ str(daytime(views[i][3])))
            Filters = {'Status': Status, 'views': views, 'DateS': Date}
            return render(request, 'indexCoordinator.html', Filters)
        if Status == 'All' and Year != 'All' and Read == 'All':
            Year = int(Year)
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE YEAR(login_contribute.Date) = '%s' AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [Year, User.objects.filter(id= request.user.id)[0].Faculty_id]
                )
                views = cursor.fetchall()
            Date = []
            for i in range(len(views)):
                Date.append(str(views[i][7]) +"/"+ str(daytime(views[i][3])))
            Filters = {'Status': Status, 'views': views, 'DateS': Date}
            return render(request, 'indexCoordinator.html', Filters)
        if Status != 'All' and Year == 'All' and Read == 'All':
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE login_contribute.Status= '%s' AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [Status, User.objects.filter(id= request.user.id)[0].Faculty_id]
                )
                views = cursor.fetchall()
            Date = []
            for i in range(len(views)):
                Date.append(str(views[i][7]) +"/"+ str(daytime(views[i][3])))
            Filters = {'Status': Status, 'views': views, 'DateS': Date}
            return render(request, 'indexCoordinator.html', Filters)
        if Status == 'All' and Year != 'All' and Read != 'All':
            Year = int(Year)
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE YEAR(login_contribute.Date) ='%s' and login_contribute.Readed = '%s' AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [Year, Read, User.objects.filter(id= request.user.id)[0].Faculty_id]
                    )
                views = cursor.fetchall()
            Date = []
            for i in range(len(views)):
                Date.append(str(views[i][7]) +"/"+ str(daytime(views[i][3])))
            Filters = {'Status': Status, 'views': views, 'DateS': Date}
            return render(request, 'indexCoordinator.html', Filters)  
        if Status != 'All' and Year == 'All' and Read != 'All':
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE login_contribute.Status= '%s' and login_contribute.Readed= '%s' AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [Status, Read, User.objects.filter(id= request.user.id)[0].Faculty_id]
                )
                views = cursor.fetchall()
            Date = []
            for i in range(len(views)):
                Date.append(str(views[i][7]) +"/"+ str(daytime(views[i][3])))
            Filters = {'Status': Status, 'views': views, 'DateS': Date}
            return render(request, 'indexCoordinator.html', Filters)
        if Status != 'All' and Year != 'All' and Read == 'All':
            Year = int(Year)
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE login_contribute.Status= '%s' and YEAR(login_contribute.Date) ='%s' AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [Status, Year, User.objects.filter(id= request.user.id)[0].Faculty_id]
                )
                views = cursor.fetchall()
            Date = []
            for i in range(len(views)):
                Date.append(str(views[i][7]) +"/"+ str(daytime(views[i][3])))
            Filters = {'Status': Status, 'views': views, 'DateS': Date}
            return render(request, 'indexCoordinator.html', Filters)
        if Status != 'All' and Year != 'All' and Read != 'All':
            Year = int(Year)
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE login_contribute.Status= '%s' and YEAR(login_contribute.Date) ='%s' and login_contribute.Readed= '%s' AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [Status, Year, Read, User.objects.filter(id= request.user.id)[0].Faculty_id]
                )
                views = cursor.fetchall()
            Date = []
            for i in range(len(views)):
                Date.append(str(views[i][7]) +"/"+ str(daytime(views[i][3])))
            Filters = {'Status': Status, 'views': views, 'DateS': Date}
            return render(request, 'indexCoordinator.html', Filters)
    else:
        return render(request, 'login.html')
def my_profileCoordinator(request):
    if request.user.is_authenticated:
        user = User.objects.filter(id = request.user.id)
        profile = {'user' : user}
        return render(request, 'my_profileCoordinator.html', profile)
    else:
        return render(request, 'login.html')