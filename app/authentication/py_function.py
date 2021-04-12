from app.authentication.schemas import PasscodeUpdate
import pandas.io.sql as psql
import pandas as pd
import sqlalchemy
from sqlalchemy.orm.session import Session
from app.configs import mailinfo
def email_config():
    return mailinfo.setting()
def fetch_data(search,engine,search_type):

    query = "SELECT * FROM "+search_type+" Where type like '"+search+"%' OR name like '"+search+"%' OR description like '"+search+"%' "#OR title like '%"+search+"%'"
        #query  = "SELECT courses.name, courses.type, courses.description FROM courses WHERE courses.name like '"+search+"%' OR courses.type like '"+search+"%' OR courses.description like '"+search+"%' UNION ALL SELECT talents.name , talents.type, talents.description FROM talents WHERE talents.name like '"+search+"%' OR talents.type like '"+search+"%' Or talents.description like '"+search+"%'"
        #query   = "SELECT * FROM courses WHERE courses.name like '"+search+"%' OR courses.type like '"+search+"%' OR courses.description like '"+search+"%' UNION ALL SELECT * FROM talents WHERE talents.name like '"+search+"%' OR talents.type like '"+search+"%' Or talents.description like '"+search+"%'"
    print(query)
    print("hello")
    df = engine.execute(sqlalchemy.text(query))
        #df = pd.read_sql(query, engine)
    print(df)
    return df
    # elif search_type == "talents":
    #     query = "SELECT * FROM talents Where type like '"+search+"%' OR name like '"+search+"%' OR description like '"+search+"%' "
    #     df = engine.execute(sqlalchemy.text(query))
    #     #df = pd.read_sql(query, engine)
    #     print(df)
    #     return df
    # else:
    #     return ("please select correct database")


import pandas as pd
from random import randint
from . import conf, models
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.talent.database import database

# def fetch_data(search,cnxn):
#     query_cols='select top 1* from SALES_DATA'
#     df=pd.read_sql(query_cols,cnxn)
#     # col_list=df.columns.tolist()
#     col_list=(",".join(df.columns))
#     print(col_list)
#     query = 'SELECT TOP 10* FROM SALES_DATA '\
#             "where lower(concat("+col_list+")) like '%"+search+"%'"
#     print(query)
#     df = pd.read_sql(query,cnxn)
#     return df
from .models import Users

def check_user_details(username,password,engine):
    query = 'select * from USERS where email='+"'"+str(username)+"'"+' and PASSWORD='+"'"+str(password)+"'"
    df= pd.read_sql(query,engine)
    return df.shape[0]


def check_user_exist(email,engine):
    query = 'select * from USERS where email='+"'"+str(email)+"'"
    df= pd.read_sql(query,engine)
    return df.shape[0]


def signup_data(firstname,lastname,city,email,password):
    query = "INSERT INTO USERS "\
            "VALUES ("+"'"+str(firstname)+"'"+",'"+str(lastname)+"'"+",'"+str(city)+"'"+"" \
            ",'"+str(email)+"','"+str(password)+"'"+")"
    print(query)
    return query

def generate_code():
    return randint(100000,1000000)

async def send_auth_code(email):
    passcode = generate_code()
    print (passcode)
    query = "Update users set passcode='" + str(passcode) + "'where email='"+ str(email)+"'"
    print(query)
    await database.execute(query)
    return passcode


def generate_register_email(username,RECEIVER_EMAIL):
    subject = "Register User"
    body ="\nHi "+str(username)+"\n\n Your registration is completed\n\n\n Thanks & Regards \nTeam Cinedarbaar"
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

def generate_login_email(username,RECEIVER_EMAIL):
    subject = "URGENT: Login Detected"
    body ="\nHi "+str(username)+"\n\nWe notice that you logged in \n\nIf it isn't You kindly reset your password \n\n\nThanks & Regards \nTeam Cinedarbaar"
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




# old section

def generate_auth_email(passcode1,RECEIVER_EMAIL):
    subject = "Verification Code"
    body ="\nHi Everyone,\n\n Your verification code is "+str(passcode1)
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

def generate_password_change_email(RECEIVER_EMAIL):
    subject = "URGENT: Password Change"
    body ="\nHi User,\n\n Your password changed successfully "
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


def validate_passcode(email,passcode,engine):
    query = "select * from USERS WHERE EMAIL='"+str(email)+"' AND PASSCODE = "+str(passcode)
    df=pd.read_sql(query,engine)
    if df.shape[0]>0:
        return True
    else:
        return False
from app.utils import util
async def update_password(email,password,confirm_password):
    query = Users.__table__.update().where(Users.email == email).values(
            password = util.get_password_hash(password),
            confirm_password = util.get_password_hash(confirm_password),
            passcode = 000000
    )
    print(query)
    await database.execute(query)