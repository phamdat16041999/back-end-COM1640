from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.db import connection
from Login.models import Contribute, Term, Data, Comment, User, Faculty
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
import pickle
import os
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def daytime(Enddate):
    Begindate = datetime.today()
    Days_remaining = Enddate - Begindate
    return Days_remaining
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep="-")
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    cred = None

    pickle_file = f"token_{API_SERVICE_NAME}_{API_VERSION}.pickle"

    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, "wb") as token:
            pickle.dump(cred, token)
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, "service created successfully")
        return service
    except Exception as e:
        print("Unable to connect!")
        print(e)
        return None
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
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Student":
        with connection.cursor() as cursor:
            cursor.execute(
            "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE login_user.id = '%s' AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [request.user.id, User.objects.filter(id= request.user.id)[0].Faculty_id]
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
        Contributes = {'views': views, 'DateS': Date, 'Year': Year}
        return render(request, 'MyContribute.html', Contributes)
    else:
        return render(request, 'login.html')
def filter(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Student":
        Year = request.POST.get('Year','')
        if Year == 'All':
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE login_user.id = '%s' AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [request.user.id, User.objects.filter(id= request.user.id)[0].Faculty_id]
                )
                views = cursor.fetchall()
        else:
            Year = int(Year)
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT login_user.username, login_contribute.Name, login_contribute.Date, login_term.FinalClosureDate, login_user.email, login_contribute.Status, login_contribute.Readed, login_contribute.id FROM login_user INNER JOIN login_contribute ON login_user.id = login_contribute.UserID_id INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm WHERE login_user.id = '%s'  AND YEAR(login_contribute.Date) = '%s' AND login_user.Faculty_id = '%s' ORDER BY login_term.FinalClosureDate", [request.user.id, Year, User.objects.filter(id= request.user.id)[0].Faculty_id]
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
        viewStudent = {'views': views, 'DateS': Date, 'Year': Year}
        return render(request, 'MyContribute.html', viewStudent)
    else:
        return render(request, 'login.html')
def ViewDeadline(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Student":
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
    else:
        return render(request, 'login.html')
def ViewDeadlineYear(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Student":
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
    else:
        return render(request, 'login.html')
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
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Student":
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT login_contribute.Document, login_contribute.Name, login_contribute.Description FROM login_contribute INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm INNER JOIN login_user ON login_contribute.UserID_id = login_user.id WHERE login_term.idTerm = '%s' and login_user.id ='%s'", [id,request.user.id]
            )
            DataNoImage = cursor.fetchall()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT login_data.Data FROM login_contribute INNER JOIN login_term ON login_contribute.TermID_id = login_term.idTerm INNER JOIN login_user ON login_contribute.UserID_id = login_user.id INNER JOIN login_data ON login_contribute.id = login_data.ContributeID_id WHERE login_term.idTerm = '%s' and login_user.id ='%s'", [id,request.user.id]
            )
            DataImage = cursor.fetchall()
        if len(DataNoImage) > 0 and len(DataImage) > 0:
            ternID = {'ternID':id, 'DataNoImage': DataNoImage,'DataImage': DataImage}
            return render(request, 'Update.html', ternID)
            # return redirect('/Student/ViewDeadline/viewUpdate/'+str(id), ternID)
        else:
            return render(request, 'viewUploaded.html', {'DataNoImage': DataNoImage,'DataImage': DataImage})
    else:
        return render(request, 'login.html')
def viewUploaded(request,id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Student":
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
    else:
        return render(request, 'login.html')
def uploadContribute(request,id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Student":
        if request.method == 'POST' and request.FILES['contribute'] and request.FILES['image1'] and request.FILES['image2']:
            nameContribute = request.POST.get('nameContribute','')
            description = request.POST.get('description','')
            contribute = request.FILES['contribute']
            image1 = request.FILES['image1']
            image2 = request.FILES['image2']
            Contribute.objects.create(Name = nameContribute, Description = description, TermID_id = id, Status = False, UserID_id = request.user.id, Document = contribute, Readed = False)
            Data.objects.create(Data = image1, ContributeID_id = Contribute.objects.latest('id').id)
            Data.objects.create(Data = image2, ContributeID_id = Contribute.objects.latest('id').id)
            # Send email
            facultyID = User.objects.filter(id = request.user.id)[0].Faculty_id
            facultyName = Faculty.objects.filter(id = facultyID)[0].Name
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT login_user.email FROM login_user INNER JOIN login_user_groups ON login_user.id = login_user_groups.user_id INNER JOIN auth_group ON login_user_groups.group_id = auth_group.id INNER JOIN login_faculty ON login_faculty.id = login_user.Faculty_id WHERE auth_group.name = %s AND login_faculty.Name = %s" ,
                    ["Coordinator",facultyName]
                )
                Email = cursor.fetchall()
            
            for i in Email:
                CLIENT_SECRET_FILE = './client_secret.json'
                API_NAME = "gmail"
                API_VERSION = "v1"
                SCOPES = ["https://mail.google.com/"]
                service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
                emailMsg = "The student whose name is "+ User.objects.filter(id = request.user.id)[0].last_name+" contributes a magazine to the term "+Term.objects.filter(idTerm=id)[0].NameTerm+".\n Please visit here to see contributions: http://localhost:8000/Coordinator/viewContribute/" +  str(Contribute.objects.latest('id').id)
                mimeMessage = MIMEMultipart()
                mimeMessage["to"] = i[0]
                mimeMessage["subject"] = "Notification"
                mimeMessage.attach(MIMEText(emailMsg, 'plain'))
                raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
                message = service.users().messages().send(userId="me", body={"raw": raw_string}).execute()
            return redirect('/Student/ViewDeadline')
        else:
            # Not found 404
            return redirect('/')
    else:
        return render(request, 'login.html')
def updateContribute(request,id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Student":
        if request.method == 'POST' and request.FILES['contribute'] and request.FILES['image1'] and request.FILES['image2']:
            nameContribute = request.POST.get('nameContribute','')
            description = request.POST.get('description','')
            contribute = request.FILES['contribute']
            image1 = request.FILES['image1']
            image2 = request.FILES['image2']
            Contribute.objects.filter(TermID_id = id, UserID_id = request.user.id).delete()
            Contribute.objects.create(Name = nameContribute, Description = description, TermID_id = id, Status = False, UserID_id = request.user.id, Document = contribute, Readed = False)
            Data.objects.create(Data = image1, ContributeID_id = Contribute.objects.latest('id').id)
            Data.objects.create(Data = image2, ContributeID_id = Contribute.objects.latest('id').id)
            # Send email
            facultyID = User.objects.filter(id = request.user.id)[0].Faculty_id
            facultyName = Faculty.objects.filter(id = facultyID)[0].Name
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT login_user.email FROM login_user INNER JOIN login_user_groups ON login_user.id = login_user_groups.user_id INNER JOIN auth_group ON login_user_groups.group_id = auth_group.id INNER JOIN login_faculty ON login_faculty.id = login_user.Faculty_id WHERE auth_group.name = %s AND login_faculty.Name = %s" ,
                    ["Coordinator",facultyName]
                )
                Email = cursor.fetchall()
            
            for i in Email:
                CLIENT_SECRET_FILE = './client_secret.json'
                API_NAME = "gmail"
                API_VERSION = "v1"
                SCOPES = ["https://mail.google.com/"]
                service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
                emailMsg = "The student whose name is "+ User.objects.filter(id = request.user.id)[0].last_name+" contributes a magazine to the term "+Term.objects.filter(idTerm=id)[0].NameTerm+".\n Please visit here to see contributions: http://localhost:8000/Coordinator/viewContribute/" +  str(Contribute.objects.latest('id').id)
                mimeMessage = MIMEMultipart()
                mimeMessage["to"] = i[0]
                mimeMessage["subject"] = "Notification"
                mimeMessage.attach(MIMEText(emailMsg, 'plain'))
                raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
                message = service.users().messages().send(userId="me", body={"raw": raw_string}).execute()
            return redirect('/Student/ViewDeadline')
        else:
            # Not found 404
            return redirect('/')
    else:
        return render(request, 'login.html')
def sendMessenger(request, id, messenger):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Student":
        ContributeID = Contribute.objects.get(TermID = id, UserID = request.user.id)
        Comment.objects.create(UserID_id = request.user.id, ContributeID_id = ContributeID.id, Comment = messenger)
        ternID = {'ternID':id}
        return render(request, 'Update.html', ternID)
    else:
        return render(request, 'login.html')
def getMessenger(request, id):
    ContributeID = Contribute.objects.get(TermID = id, UserID = request.user.id)
    comment = Comment.objects.filter(ContributeID_id = ContributeID.id)
    html = []
    for i in comment:
        if getAuthGroup(i.UserID_id) == "Student":
            html.append("<span class='you first'>"+i.Comment+" <span class='time'>"+i.DateComment.strftime("%m/%d/%y, %H:%M:%S")+"</span></span>")
        if getAuthGroup(i.UserID_id) == "Coordinator":
            html.append("<span class='friend last'>"+i.Comment+"<span class='time'>"+i.DateComment.strftime("%m/%d/%y, %H:%M:%S")+"</span></span>")
    response = HttpResponse()
    response.writelines(html)
    return response
# def Update(request,id):
#     if request.user.is_authenticated and getAuthGroup(request.user.id) == "Student":
#         if request.user.is_authenticated:
#             if request.method == 'POST' and request.FILES['contribute'] and request.FILES['image1'] and request.FILES['image2']:
#                 nameContribute = request.POST.get('nameContribute','')
#                 description = request.POST.get('description','')
#                 contribute = request.FILES['contribute']
#                 image1 = request.FILES['image1']
#                 image2 = request.FILES['image2']
#                 Contribute.objects.filter(TermID_id = id,UserID_id = request.user.id).delete()
#                 Contribute.objects.create(Name = nameContribute, Description = description, TermID_id = id, Status = False, UserID_id = request.user.id, Document = contribute)
#                 Data.objects.create(Data = image1, ContributeID_id = Contribute.objects.latest('id').id)
#                 Data.objects.create(Data = image2, ContributeID_id = Contribute.objects.latest('id').id)
#                 # Contribute.objects.create()
#                 return redirect('/Student/ViewDeadline/viewUpdate/'+str(id))
#             else:
#                 # Not found 404
#                 return redirect('/')
#         else:
#             return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')
def my_profileStudent(request):
    if request.user.is_authenticated:
        user = User.objects.filter(id = request.user.id)
        profile = {'user' : user}
        return render(request, 'my_profileStudent.html', profile)
    else:
        return render(request, 'login.html')
