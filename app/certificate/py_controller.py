
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.configs import mailinfo
def email_config():
    return mailinfo.setting()

def generate_certificate_email(username,RECEIVER_EMAIL):
    subject = "Request for Certificate"
    body ="Hello "+str(username)+" greetings from cinedarbaar \n\n Your request is logged in our system \n You will soon receive a mail with your certificate "
    "\n\n Regards\nTeam Cinedarbaar"
    sender_email = email_config().email_id
    receiver_email = RECEIVER_EMAIL
    password = email_config().email_pwd

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    context = ssl.create_default_context()
    
    #with smtplib.SMTP_SSL("smtpout.secureserver.net", 465, context=context) as server:

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)