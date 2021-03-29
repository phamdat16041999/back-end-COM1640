from django.shortcuts import render
from django.db import connection
from Login.models import Contribute, Term, Data, Comment, User, Faculty
from datetime import datetime

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
def indexManager(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Manager":
        return render(request, 'indexManager.html')
    else:
        return render(request, 'login.html')
def viewContributionManager(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Manager":
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
        viewManager = {'views': views, 'DateS': Date, 'Year': Year}
        return render(request, 'viewContributionManager.html', viewManager)
    else:
        return render(request, 'login.html')
def Contributionofterms(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Manager":
        return render(request, 'ContributionOfTearms.html')
    else:
        return render(request, 'login.html')
def Percentageofcontributionscontributetoeachfaculty(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Manager":
        return render(request, 'Percentageofcontributionscontributetoeachfaculty.html')
    else:
        return render(request, 'login.html')
def Numberofstudentssubmittingallsubjectsineachterm(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Manager":
        return render(request, 'Numberofstudentssubmittingallsubjectsineachterm.html')
    else:
        return render(request, 'login.html')
def Exercisesthatthecoordinatorhasnotreadyet(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Manager":
        return render(request, 'Exercisesthatthecoordinatorhasnotreadyet.html')
    else:
        return render(request, 'login.html')
def filter(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Manager":
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
            viewManager = {'views': views, 'DateS': Date, 'Year': Year}
            return render(request, 'viewContributionManager.html', viewManager)
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
            viewManager = {'views': views, 'DateS': Date, 'Year': Year}
            return render(request, 'viewContributionManager.html', viewManager)
    else:
        return render(request, 'login.html')
def my_profileManager(request):
    if request.user.is_authenticated:
        user = User.objects.filter(id = request.user.id)
        profile = {'user' : user}
        return render(request, 'my_profileManager.html', profile)
    else:
        return render(request, 'login.html')