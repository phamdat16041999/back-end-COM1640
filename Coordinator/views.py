from django.shortcuts import render
from django.db import connection
from datetime import datetime, date
from datetime import timedelta 
from Login.models import User
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
        # views[0][3].strftime("%Y,%m,%d, %H:%M:%S")
        # datetime.strptime(views[0][3], "%Y,%m,%d, %H:%M:%S")
        Date = []
        for i in range(len(views)):
           Date.append(str(views[i][7]) +"/"+ str(daytime(views[i][3])))

        viewCoordinator = {'views': views, 'DateS': Date}
        return render(request, 'indexCoordinator.html', viewCoordinator)
    else:
        return render(request, 'login.html')


def viewContribute(request):
    return render(request, 'viewContribute.html')