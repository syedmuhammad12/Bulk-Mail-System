from django.shortcuts import render,HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import connection
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
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
from datetime import date


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
    invoice = request.FILES.getlist('invoice_file')
    
    if emails.name.endswith(".txt"):
        mails = list(map(lambda x: x.decode().strip(), emails.readlines()))
    elif emails.name.endswith(".csv"):
        paramFile = emails.read().decode('iso-8859-1')
        paramFile = io.StringIO(paramFile)
        portfolio = csv.reader(paramFile)
        mails = [i[0] for i in portfolio]
    print(mails)
    email = EmailMessage(
    subject,
    description,
    settings.EMAIL_HOST_USER,
    bcc=mails,
    )
    for i in invoice:
        email.attach(i.name, i.read(), i.content_type)
    email.send()
        
    return redirect('index')

def send_mail(name, email, emailId, password, bodyFile, subjectWord, file_exe_name):
    #=======================================================================================================================
    today = date.today()
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
    num = randint(111111111, 999999999)
    newMessage['Subject'] = subject
    newMessage['From'] = f"{name}{num}<{emailId}>"
    newMessage['To'] = email
    transaction_id = randint(100000000, 999999999)
    random_id = randint(100000000, 999999999)
    xyz_id = (uuid.uuid4())
#=======================================================================================================================
    # Mail Body Content
    body = open(bodyFile, 'r').read()
    body = body.replace('$email', email)
    body = body.replace('$name', name)
    body = body.replace('$product_no', rand_string + str(randint(10000, 99999)))
    body = body.replace('$invoice_no', str(transaction_id))
    body = body.replace('$digi_no', str(xyz_id))
    body = body.replace('$date', str(date))
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
#=======================================================================================================================
    # saving the changes to html_code.html
    try:
        with open('html_code.html', 'w') as f:
            f.write(html)
            f.close
#=======================================================================================================================
        file = str(file_exe_name) + str(invoiceNo) + ".pdf"
        # pdfkit.from_file('html_code.html', file, configuration=config)
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
    newMessage.attach(MIMEText(body))
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
        mailserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mailserver.login(emailId, password)
        mailserver.sendmail(emailId, email, newMessage.as_string())
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
