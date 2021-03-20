from django.shortcuts import render
from django.db import connection
# Create your views here.
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
