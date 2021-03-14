from django.shortcuts import render
from django.db import connection
from datetime import datetime 
from datetime import timedelta 
from datetime import date 

def getAuthGroup(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT auth_group.name FROM auth_group INNER JOIN login_user_groups ON auth_group.id = login_user_groups.group_id INNER JOIN login_user ON login_user.id = login_user_groups.user_id WHERE login_user.id = '%s'" ,
            [UserID]
        )
        auth_group = cursor.fetchall()[0][0]
    return auth_group
def indexCoordinator(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Coordinator":
        return render(request, 'indexCoordinator.html')
    else:
        return render(request, 'login.html')

def days(request):
    Begindatestring = date.today() 
    print(f"Beginning date: {Begindatestring}") 
    Enddate = Begindatestring + timedelta(days=14) 
    date1 = Enddate - Begindatestring
    print(f"Ending date: {Enddate}") 
    print(date1)
def viewContribute(request):
    return render(request, 'viewContribute.html')