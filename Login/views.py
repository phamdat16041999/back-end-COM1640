
from django.shortcuts import render
import string
import random
import pickle
import os
import base64
import mysql.connector
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect

mydb = mysql.connector.connect(             #connect db
        host="localhost",
        port="3306",
        user="root",
        password="",
        database="manazinecontributions"
        ) 
	
def random_code(length):
    LETTERS = string.ascii_letters
    DIGITS = string.digits
    x = list(f'{LETTERS}{DIGITS}')
    random.shuffle(x)
    code = random.choices(x, k = length)
    code = ''.join(code)
    return(code)
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep="-")
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f"token_{API_SERVICE_NAME}_{API_VERSION}.pickle"
    # print(pickle_file)

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

def index(request):
	return render(request, 'login.html')
def forgotPassword(request):
	return render(request, 'forgotPassword.html')
def randomCode(request):
	if request.method == 'POST':    # Send email
        Codes = random_code(12)
		Email = request.POST.get('Email','')

        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM `table` WHERE email= '{Email}'")   #kiểm tra mail có trong db
        resultdb = str(mycursor.fetchone())
        if resultdb != "None":
            CLIENT_SECRET_FILE = './client_secret.json'
            API_NAME = "gmail"
            API_VERSION = "v1"
            SCOPES = ["https://mail.google.com/"]
            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
            emailMsg = random
            mimeMessage = MIMEMultipart()
            mimeMessage["to"] = Email      
            mimeMessage["subject"] = "Authentic"
            mimeMessage.attach(MIMEText(emailMsg, 'plain'))
            raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            message = service.users().messages().send(userId="me", body={"raw": raw_string}).execute()

            mycursor.execute(f"SELECT ID FROM `table` WHERE email= '{Email}'")
            ID = mycursor.fetchone()
		# Lấy ID tài khoản có email vừa gửi.
            mycursor.execute(f"UPDATE `table` SET code= Codes WHERE id= ID")   # Lưu Code vào trong DB tài khoản có ID vừa lấy
		    return redirect('/authenticationInterface/'+ID)
        else:  
            error = {'error': 'Email not exists, Please try another Email!'}
            return render(request, 'forgotPassword.html', error)
    
    return render(request, 'forgotPassword.html')
def authenticationInterface(request, id):
	userId = {'userId', id}
	return render(request, 'login.html', code)
def authentication(request, id):
    mycursor.execute(f"SELECT code FROM `table` WHERE id= ID")  # Lẫy mã đã lưu trong database từ ID
	NewCode = request.POST.get('Code','')
    if NewCode == Codes:        # So sánh hai cái với nhau
        userId = {'userId', id}
        return redirect('/authentication/'+userId)
    else:
        error = {'error': 'Wrong code!, Please try another code!'}
        return render(request, 'forgotPassword.html', error)

def indexStudent(request):
    if request.method == 'POST':
        userName = request.POST.get('userName','')
        passWord = request.POST.get('passWord','')
        user = authenticate(username=userName, password=passWord)
        if(user is not None):
            request.session.set_expiry(86400)
            auth_login(request, user)
            return redirect('/indexStudent')
        else:
            error = {'error': 'Username already exists, please try a different username'}
            return render(request, 'login.html', error)
    else:
        if request.user.is_authenticated:
            return render(request, 'indexStudent.html')
        else:
            return render(request, 'login.html')
def logout(request):
    django_logout(request)
    return render(request, 'login.html')

