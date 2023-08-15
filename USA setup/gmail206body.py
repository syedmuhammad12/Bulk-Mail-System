#=======================================================================================================================
import pandas as pd
from random import randint, choices
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import logging
import time
import sys
import pdfkit
import os
import string
from datetime import date
import uuid
import datetime
#=======================================================================================================================
today = date.today()
date_and_time = today.strftime("%d_%B_%Y")
#=======================================================================================================================
current_time = datetime.datetime.now()
date = str(current_time.day) + "-" + str(current_time.month) + "-" + str(current_time.year)
#=======================================================================================================================
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
#=======================================================================================================================
logging.basicConfig(filename='mail.log', level=logging.DEBUG)
#=======================================================================================================================
totalSend = 1
if(len(sys.argv) > 1):
    totalSend = int(sys.argv[1])
#=======================================================================================================================
emaildf = pd.read_csv('gmail.csv')
contactsData = pd.read_csv('contacts.csv')
subjects = pd.read_csv('subject.csv')
#sender_name = pd.read_csv('sender_name.csv')
#=======================================================================================================================
f = open("tfn.txt", "r")
tfn = f.read()
bodies = ['body.txt','body1.txt','body2.txt','body3.txt','body4.txt','body5.txt','body6.txt','body7.txt','body8.txt','body9.txt','body10.txt','body11.txt','body12.txt','body13.txt','body14.txt','body15.txt','body16.txt','body17.txt','body18.txt','body19.txt','body20.txt','body21.txt','body22.txt','body23.txt','body24.txt','body25.txt','body26.txt','body27.txt','body28.txt','body29.txt','body30.txt','body31.txt','body32.txt','body33.txt','body34.txt','body35.txt','body36.txt','body37.txt','body38.txt','body39.txt','body40.txt','body41.txt','body42.txt','body43.txt','body44.txt','body45.txt','body46.txt','body47.txt','body48.txt','body49.txt','body50.txt','body51.txt','body52.txt','body53.txt','body54.txt','body55.txt','body56.txt','body57.txt','body58.txt','body59.txt','body60.txt','body61.txt','body62.txt','body63.txt','body64.txt','body65.txt','body66.txt','body67.txt','body68.txt','body69.txt','body70.txt','body71.txt','body72.txt','body73.txt','body74.txt','body75.txt','body76.txt','body77.txt','body78.txt','body79.txt','body80.txt','body81.txt','body82.txt','body83.txt','body84.txt','body85.txt','body86.txt','body87.txt','body88.txt','body89.txt','body90.txt','body91.txt','body92.txt','body93.txt','body94.txt','body95.txt','body96.txt','body97.txt','body98.txt','body99.txt','body100.txt','body101.txt','body102.txt','body103.txt','body104.txt','body105.txt','body106.txt','body107.txt','body108.txt','body109.txt','body110.txt','body111.txt','body112.txt','body113.txt','body114.txt','body115.txt','body116.txt','body117.txt','body118.txt','body119.txt','body120.txt','body121.txt','body122.txt','body123.txt','body124.txt','body125.txt','body126.txt','body127.txt','body128.txt','body129.txt','body130.txt','body131.txt','body132.txt','body133.txt','body134.txt','body135.txt','body136.txt','body137.txt','body138.txt','body139.txt','body140.txt','body141.txt','body142.txt','body143.txt','body144.txt','body145.txt','body146.txt','body147.txt','body148.txt','body149.txt','body150.txt','body151.txt','body152.txt','body153.txt','body154.txt','body155.txt','body156.txt','body157.txt','body158.txt','body159.txt','body160.txt','body161.txt','body162.txt','body163.txt','body164.txt','body165.txt','body166.txt','body167.txt','body168.txt','body169.txt','body170.txt','body171.txt','body172.txt','body173.txt','body174.txt','body175.txt','body176.txt','body177.txt','body178.txt','body179.txt','body180.txt','body181.txt','body182.txt','body183.txt','body184.txt','body185.txt','body186.txt','body187.txt','body188.txt','body189.txt','body190.txt','body191.txt','body192.txt','body193.txt','body194.txt','body195.txt','body196.txt','body197.txt','body198.txt','body199.txt','body200.txt']
file_exe_name = ['Invoice_' + date_and_time, 'Bill_' + date_and_time, 'Receipt_' + date_and_time, 'Statement_' + date_and_time]
#===========================================================================================================================================================
#=======================================================================================================================
def send_mail(name, email, emailId, password, bodyFile, subjectWord, file_exe_name):
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
    html = html.replace('$tfn', tfn)
    html = html.replace('$date', date)
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
        print(f"send to {email} by {emailId} successfully : {totalSend}")
        logging.info(
            f"send to {email} by {emailId} successfully : {totalSend}")
#=======================================================================================================================
    except UnboundLocalError as fileerror:
        print(fileerror)
        logging.error(fileerror)
        # remove_email(emailId, password)
#=======================================================================================================================
    except smtplib.SMTPResponseException as e:
        print(e)
        error_code = e.smtp_code
        error_message = e.smtp_error
        print(f"send to {email} by {emailId} failed")
        logging.info(f"send to {email}  by {emailId} failed")
        print(f"error code: {error_code}")
        print(f"error message: {error_message}")
        logging.info(f"error code: {error_code}")
        logging.info(f"error message: {error_message}")
#=======================================================================================================================
        remove_email(emailId, password)
#=======================================================================================================================
def start_mail_system():
    global totalSend
    j = 0
    k = 0
    l = 0
    m = 0
    o = 0
#=======================================================================================================================
    for i in range(len(contactsData)):
        emaildf = pd.read_csv('gmail.csv')
        if(j >= len(emaildf)):
            j = 0
#=======================================================================================================================
        time.sleep(0)
        send_mail(contactsData.iloc[i]['name'], contactsData.iloc[i]['email'], emaildf.iloc[j]['email'],
                  emaildf.iloc[j]['password'], bodies[k], subjects.iloc[l]['subject'], file_exe_name[o])
        totalSend += 1
#=======================================================================================================================
#=======================================================================================================================
        j = j + 1
        k = k + 1
        l = l + 1
        m = m+1
        o = o+1
#=======================================================================================================================
#=======================================================================================================================
        if j == len(emaildf):
            j = 0
        if k == len(bodies):
            k = 0
        if l == len(subjects):
            l = 0
        if o == len(file_exe_name):
            o = 0
#=======================================================================================================================
    quit()
#=======================================================================================================================
def remove_email(emailId, password):
    df = pd.read_csv('gmail.csv')
    index = df[df['email'] == emailId].index
    df.drop(index, inplace=True)
    df.to_csv('gmail.csv', index=False)
    print(f"{emailId} removed from gmail.csv")
    logging.info(f"{emailId} removed from gmail.csv")
#=======================================================================================================================
try:
    for i in range(6):
        start_mail_system()
except KeyboardInterrupt as e:
    print(f"\n\ncode stopped by user")
#=======================================================================================================================
# CODE END FROM HERE................................
#=======================================================================================================================