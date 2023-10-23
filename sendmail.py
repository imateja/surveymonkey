#!/usr/local/bin/python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import sys
import json

load_dotenv()

sender_email = os.getenv("EMAILSND")
sender_password = os.getenv("EMAILPW")

content = sys.argv[1]
recipientsjson = json.loads(sys.argv[2])

recipients = [recipient['email'] for recipient in recipientsjson]

subject = "crazy cool survey"
body = "Please take our newest survey: "+content
message = MIMEMultipart()
message['From'] = sender_email
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()  
    server.login(sender_email, sender_password)
    for recipient_email in recipients:
        server.sendmail(sender_email, recipient_email, message.as_string())  
    print("sent e-mails successfully")
