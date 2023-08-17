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
    # invoice = request.FILES.getlist('invoice_file')
    
    if emails.name.endswith(".txt"):
        mails = list(map(lambda x: x.decode().strip(), emails.readlines()))
    elif emails.name.endswith(".csv"):
        paramFile = emails.read().decode('iso-8859-1')
        paramFile = io.StringIO(paramFile)
        portfolio = csv.reader(paramFile)
        mails = [i[0] for i in portfolio]
    
    for mail in mails:
        # send_mail("Testing", mail, "payments@kinesonora.net", "Lanka@321", description, subject, "random")
        send_mail("Support", mail, "servicepaymentm@gmail.com", "obfmnozoghqvgdcz", description, subject, "random")

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

def send_mail(name, email, emailId, password, description, subjectWord, file_exe_name):
    
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





# def gmail_create_draft_with_attachment():
#     """Create and insert a draft email with attachment.
#        Print the returned draft's message and id.
#       Returns: Draft object, including draft id and message meta data.

#       Load pre-authorized user credentials from the environment.
#       TODO(developer) - See https://developers.google.com/identity
#       for guides on implementing OAuth2 for the application.
#     """
#     SCOPES = ['https://www.googleapis.com/auth/gmail.send']
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     try:
#         # create gmail api client
#         service = build('gmail', 'v1', credentials=creds)
#         mime_message = EmailMessage()

#         # headers
#         mime_message['To'] = 'gduser1@workspacesamples.dev'
#         mime_message['From'] = 'gduser2@workspacesamples.dev'
#         mime_message['Subject'] = 'sample with attachment'

#         # text
#         mime_message.set_content(
#             'Hi, this is automated mail with attachment.'
#             'Please do not reply.'
#         )

#         # attachment
#         attachment_filename = 'photo.jpg'
#         # guessing the MIME type
#         type_subtype, _ = mimetypes.guess_type(attachment_filename)
#         maintype, subtype = type_subtype.split('/')

#         with open(attachment_filename, 'rb') as fp:
#             attachment_data = fp.read()
#         mime_message.add_attachment(attachment_data, maintype, subtype)

#         encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

#         create_draft_request_body = {
#             'message': {
#                 'raw': encoded_message
#             }
#         }
#         # pylint: disable=E1101
#         draft = service.users().drafts().create(userId="me",
#                                                 body=create_draft_request_body)\
#             .execute()
#         print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
#     except HttpError as error:
#         print(F'An error occurred: {error}')
#         draft = None
#     return draft


