from django.shortcuts import render,HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import connection
from django.conf import settings
import csv
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from random import randint, choices
import string
import uuid
import datetime
from datetime import date as datee
import pdfkit
import os
import time

import base64
import mimetypes
import os
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Create your views here.
def index(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'index.html')

def sendemail(request):
    logo = request.FILES.get('logo')
    emails = request.FILES.get('emails_file')
    subject = request.POST.get('email_subject')
    description = request.POST.get('email_description')
    name_person = request.POST.get('name_of_person')
    # invoice = request.FILES.getlist('invoice_file')
    
    if emails.name.endswith(".txt"):
        mails = list(map(lambda x: x.decode().strip(), emails.readlines()))
    elif emails.name.endswith(".csv"):
        paramFile = emails.read().decode('iso-8859-1')
        paramFile = io.StringIO(paramFile)
        portfolio = csv.reader(paramFile)
        mails = [i[0] for i in portfolio]
    
    # for mail in mails:
        # send_mail("Testing", mail, "payments@kinesonora.net", "Lanka@321", description, subject, "random")
        # if "@gmail.com" in mail:
    send_mail(name_person, mails, "syedmuhammad1111@gmail.com", description, subject, "Bill")
        # else:
        # send_email("Customer", mail, "support@Digicoinz.net", "6d8511f3-9efd-420d-9f8e-81408cd14243", description, subject, "random")
    time.sleep(1)
    # print(mails)
    # email = EmailMessage(
    # subject,
    # description,
    # settings.EMAIL_HOST_USER,
    # bcc=mails,
    # )
    # for i in invoice:
    #     email.attach(i.name, i.read(), i.content_type)
    # email.send()
        
    return redirect('index')

def send_mail(name, email, emailId, description, subjectWord, file_exe_name):
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(host='localhost', port=50001)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    #=======================================================================================================================
    today = datee.today()
    date_and_time = today.strftime("%d_%B_%Y")
    #=======================================================================================================================
    current_time = datetime.datetime.now()
    date = str(current_time.day) + "-" + str(current_time.month) + "-" + str(current_time.year)
    newMessage = MIMEMultipart()
    #=======================================================================================================================
    # [Invoice Number and Subject]
    #=======================================================================================================================
    invoiceNo = randint(1000000, 9999999)
    transaction_id = randint(10000000000, 99999999999)
    rand_string = ''.join(choices(string.ascii_uppercase, k=5))
    num = randint(111111111, 999999999)
    # subject = subjectWord + rand_string + str(invoiceNo)
    subject = subjectWord
    num = randint(111111111, 999999999)
    newMessage['Subject'] = subject
    newMessage['From'] = f"{name}<{emailId}>"
    #newMessage['From'] = name
    # newMessage['To'] = ",".join(email)
    newMessage['bcc'] = ",".join(email)
    transaction_id = randint(100000000, 999999999)
    random_id = randint(100000000, 999999999)
    xyz_id = (uuid.uuid4())
    #=======================================================================================================================
    # Mail Body Content
    # body = open(bodyFile, 'r').read()
    # body = body.replace('$email', email)
    # body = body.replace('$name', name)
    # body = body.replace('$product_no', rand_string + str(randint(10000, 99999)))
    # body = body.replace('$invoice_no', str(transaction_id))
    # body = body.replace('$digi_no', str(xyz_id))
    # body = body.replace('$date', str(date))
    #=======================================================================================================================
        # Mail PDF File
    html = open('html_code.html', 'r').read()
    # html = html.replace('$email', email)
    html = html.replace('$invoice_no', str(transaction_id))
    html = html.replace('$cus_name', name)
    # html = html.replace('$cus_email', email)
    html = html.replace('$digi_no', str(xyz_id))
    # html = html.replace('$tfn', tfn)
    html = html.replace('$date', date)
    description = "<br>".join(list(description.splitlines()))
    description = f"<p1 style='font-family: Roboto; font-size: 13pt'>{description}</p1>"
    
    #========================================================================================================================
    newMessage.attach(MIMEText(description, 'html'))
    # newMessage.attach(MIMEText(html, 'html'))
    #=======================================================================================================================
    # saving the changes to html_code.html
    try:
        with open('html_code_1.html', 'w') as f:
            f.write(html)
            f.close
    #=======================================================================================================================
        file = str(file_exe_name) + str(invoiceNo) + ".pdf"
        pdfkit.from_file('html_code_1.html', file, configuration=config)
    #=======================================================================================================================
        # html = open('html_code.html', 'r').read()
        # html = html.replace(str(transaction_id), '$invoice_no')
        # html = html.replace(name, '$cus_name')
        # html = html.replace(email, '$cus_email')
        # html = html.replace(str(xyz_id), '$digi_no')
        # html = html.replace(email, '$email')
        # with open('html_code.html', 'w') as f:
        #     f.write(html)
        #     f.close
    #=======================================================================================================================
    except PermissionError as e:
        print(e)
        #remove_email(emailId, password)
    #=======================================================================================================================
    
    #=======================================================================================================================
    try:
        service = build('gmail', 'v1', credentials=creds)
        with open(file, 'rb') as f:
            payload = MIMEBase('application', 'octet-stream', Name=file)
            # payload = MIMEBase('application', 'pdf', Name=pdfname)
            payload.set_payload(f.read())
        #=======================================================================================================================
            # enconding the binary into base64
            encoders.encode_base64(payload)
        #=======================================================================================================================
            # add header with pdf name
            payload.add_header('Content-Decomposition',
                               'attachment', filename=file)
            newMessage.attach(payload)
        #=======================================================================================================================
        # mailserver = smtplib.SMTP_SSL('mail.privateemail.com', 465)
        # mailserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # mailserver.login(emailId, password)
        # mailserver.sendmail(emailId, email, newMessage.as_string())
        encoded_message = base64.urlsafe_b64encode(newMessage.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }
#=======================================================================================================================
        # mailserver.quit()
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
#=======================================================================================================================
        os.remove(file)
        os.remove("html_code_1.html")
#=======================================================================================================================
        
#=======================================================================================================================
    # except UnboundLocalError as fileerror:
    #     print(fileerror)
        # remove_email(emailId, password)
#=======================================================================================================================
    # except smtplib.SMTPResponseException as e:
    #     print(e)
    #     error_code = e.smtp_code
    #     error_message = e.smtp_error
    #     print(f"send to {email} by {emailId} failed")
        
    #     print(f"error code: {error_code}")
    #     print(f"error message: {error_message}")
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None


def send_email(name, email, emailId, password, description, subjectWord, file_exe_name):
    
    #=======================================================================================================================
    today = datee.today()
    date_and_time = today.strftime("%d_%B_%Y")
    #=======================================================================================================================
    current_time = datetime.datetime.now()
    date = str(current_time.day) + "-" + str(current_time.month) + "-" + str(current_time.year)
    newMessage = MIMEMultipart()
    #=======================================================================================================================
    # [Invoice Number and Subject]
    #=======================================================================================================================
    invoiceNo = randint(1000000, 9999999)
    transaction_id = randint(10000000000, 99999999999)
    rand_string = ''.join(choices(string.ascii_uppercase, k=5))
    num = randint(111111111, 999999999)
    subject = subjectWord + rand_string + str(invoiceNo)
    # subject = subjectWord
    num = randint(111111111, 999999999)
    newMessage['Subject'] = subject
    # newMessage['From'] = f"{name}{num}<{emailId}>"
    #newMessage['From'] = name
    newMessage['To'] = email
    transaction_id = randint(100000000, 999999999)
    random_id = randint(100000000, 999999999)
    xyz_id = (uuid.uuid4())
    #=======================================================================================================================
    # Mail Body Content
    # body = open(bodyFile, 'r').read()
    # body = body.replace('$email', email)
    # body = body.replace('$name', name)
    # body = body.replace('$product_no', rand_string + str(randint(10000, 99999)))
    # body = body.replace('$invoice_no', str(transaction_id))
    # body = body.replace('$digi_no', str(xyz_id))
    # body = body.replace('$date', str(date))
    #=======================================================================================================================
        # Mail PDF File
    html = open('html_code.html', 'r').read()
    html = html.replace('$email', email)
    html = html.replace('$invoice_no', str(transaction_id))
    html = html.replace('$cus_name', name)
    html = html.replace('$cus_email', email)
    html = html.replace('$digi_no', str(xyz_id))
    # html = html.replace('$tfn', tfn)
    html = html.replace('$date', date)
    
    description = f"<strong style='font-family: brush script mt; font-weight: bold; font-style: italic; font-size: 18pt'>{description}</strong>"
    
    #========================================================================================================================
    newMessage.attach(MIMEText(description, 'html'))
    # newMessage.attach(MIMEText(html, 'html'))
    #=======================================================================================================================
    # saving the changes to html_code.html
    try:
        with open('html_code.html', 'w') as f:
            f.write(html)
            f.close
    #=======================================================================================================================
        file = str(file_exe_name) + str(invoiceNo) + ".pdf"
        pdfkit.from_file('html_code.html', file, configuration=config)
    #=======================================================================================================================
        html = open('html_code.html', 'r').read()
        html = html.replace(str(transaction_id), '$invoice_no')
        html = html.replace(name, '$cus_name')
        html = html.replace(email, '$cus_email')
        html = html.replace(str(xyz_id), '$digi_no')
        html = html.replace(email, '$email')
        with open('html_code.html', 'w') as f:
            f.write(html)
            f.close
    #=======================================================================================================================
    except PermissionError as e:
        print(e)
        #remove_email(emailId, password)
    #=======================================================================================================================
    
    #=======================================================================================================================
    try:
        
        with open(file, 'rb') as f:
            payload = MIMEBase('application', 'octet-stream', Name=file)
            # payload = MIMEBase('application', 'pdf', Name=pdfname)
            payload.set_payload(f.read())
        #=======================================================================================================================
            # enconding the binary into base64
            encoders.encode_base64(payload)
        #=======================================================================================================================
            # add header with pdf name
            payload.add_header('Content-Decomposition',
                               'attachment', filename=file)
            newMessage.attach(payload)
        #=======================================================================================================================
        # mailserver = smtplib.SMTP_SSL('smtp-relay.sendinblue.com', 465)
        mailserver = smtplib.SMTP('smtp.postmarkapp.com', 587)
        mailserver.starttls()
        # mailserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mailserver.login("6d8511f3-9efd-420d-9f8e-81408cd14243", password)
        # mailserver.login(emailId, password)
        mailserver.sendmail(emailId, email, newMessage.as_string())
        encoded_message = base64.urlsafe_b64encode(newMessage.as_bytes()).decode()
#=======================================================================================================================
        mailserver.quit()
#=======================================================================================================================
        os.remove(file)
#=======================================================================================================================
        
#=======================================================================================================================
    except UnboundLocalError as fileerror:
        print(fileerror)
        # remove_email(emailId, password)
#=======================================================================================================================
    except smtplib.SMTPResponseException as e:
        print(e)
        error_code = e.smtp_code
        error_message = e.smtp_error
        print(f"send to {email} by {emailId} failed")
        
        print(f"error code: {error_code}")
        print(f"error message: {error_message}")


