''' You work at a company that sends daily reports to clients via email. The goal of this project is to automate the process of sending these reports via email.

Here are the steps you can take to automate this process:

    Use the smtplib library to connect to the email server and send the emails.

    Use the email library to compose the email, including the recipient's email address, the subject, and the body of the email.

    Use the os library to access the report files that need to be sent.

    Use a for loop to iterate through the list of recipients and send the email and attachment.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the emails that have been sent and any errors that may have occurred during the email sending process. '''

# 1. Importing necessary libraries
import json
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# 2. Reading JSON file with credentials
with open('./credentials.json') as credentials:
    credentials = json.load(credentials)

sender_mail  = credentials['sender_mail']
password = credentials['password']
receivers_mails = credentials['receipents']
    
# 3. Prepare the MAIL content
message = MIMEMultipart()
message['From'] = sender_mail
message['Subject'] = "Automated Mail with Files Attached"

message_body = "This is an Automated Mail developed using Python"
message.attach(MIMEText(message_body, 'plain'))

# 4. Fetching Report Files
base_path = "./report_files/"
file_paths = os.listdir(base_path)
files = {}
for file_path in file_paths:
    files[file_path] = open(base_path+file_path, "rb").read()

# 5. Prepare Attachments
for path in files.keys():
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(files[path])
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % path)
    message.attach(p)

# 6. Create Session object and use that to send MAILs to All Receivers
for receiver in receivers_mails:
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_mail, password)
    message['To'] = receiver
    print (receiver)
    session.sendmail(sender_mail, receiver, message.as_string())
    session.quit()