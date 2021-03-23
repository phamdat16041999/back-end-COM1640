from django.shortcuts import render
from django.db import connection
from datetime import datetime
from Login.models import User

def daytime(Enddate):
    Begindate = datetime.today()
    Days_remaining = Enddate - Begindate
    return Days_remaining
def getAuthGroup(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT auth_group.name FROM auth_group INNER JOIN login_user_groups ON auth_group.id = login_user_groups.group_id INNER JOIN login_user ON login_user.id = login_user_groups.user_id WHERE login_user.id = '%s'" ,
            [UserID]
        )
        auth_group = cursor.fetchall()[0][0]
    return auth_group
def indexGuess(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Guess":
        with connection.cursor() as cursor:
            cursor.execute(
            "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE login_contribute.Status = 1 AND login_contribute.Readed = 1 AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [User.objects.filter(id= request.user.id)[0].Faculty_id]
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
        viewGuess = {'views': views, 'DateS': Date, 'Year': Year}
        return render(request, 'indexGuess.html', viewGuess)
    else:
        return render(request, 'login.html')
def filter(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Guess":
        Year = request.POST.get('Year','')
        if Year == 'All':
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE login_contribute.Status = 1 AND login_contribute.Readed = 1 AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [User.objects.filter(id= request.user.id)[0].Faculty_id]
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
            viewGuess = {'views': views, 'DateS': Date, 'Year': Year}
            return render(request, 'indexGuess.html', viewGuess)
        else:
            Year = int(Year)
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE login_contribute.Status = 1 AND login_contribute.Readed = 1 AND YEAR(login_contribute.Date) = '%s' AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [Year, User.objects.filter(id= request.user.id)[0].Faculty_id]
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
            viewGuess = {'views': views, 'DateS': Date, 'Year': Year}
        return render(request, 'indexGuess.html', viewGuess)
    else:
        return render(request, 'login.html')
def my_profileGuess(request):
    if request.user.is_authenticated:
        user = User.objects.filter(id = request.user.id)
        profile = {'user' : user}
        return render(request, 'my_profileGuess.html', profile)
    else:
        return render(request, 'login.html')
