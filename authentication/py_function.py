import pandas.io.sql as psql
import pandas as pd
def fetch_data(search,engine,search_type):
#     query_cols = "SELECT * FROM database-1"
#     df=pd.read_sql(query_cols,engine)
#     col_list=(','.join(df.columns))
#     print(col_list)

#     query = 'SELECT TOP 10 FROM Users'\
#                   "where lower(concat("+col_list+") like '%"+search+"%'"
    query =" SELECT * FROM "+search_type+" where type like '%"+search+"%'"

    print(query)
    df = pd.read_sql(query,engine)
    return df
import pandas as pd
from random import randint
from . import conf, models
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from talent.database import database
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
from. models import Users

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

async def send_auth_code(email,database):
    code = generate_code()
    print (code)
    query = "Update users set passcode='" + str(code) + "'where email="+ str(email)+""
    #query = "UPDATE USERS SET PASSCODE ='" + str(code) + "' where EMAIL='" + str(email) + "'"
    #query="select * from USERS where EMAIL='"+str(email)+"' AND UPDATE USERS WITH PASSCODE ="+str(code)+"where EMAIL='"+str(email)+"'"
    # query = Users.__table__.update().\
    #     where(Users.email == email).\
    #         values(
    #            passcode =code,
    #            status = "2"
    #         )
    await database.execute(query)
    return code


def generate_auth_email(passcode,RECEIVER_EMAIL):
    subject = "Verification Code"
    body ="\nHi Everyone,\n\n Your verification code is "+str(passcode)
    sender_email = conf.EMAIL_ID
    receiver_email = RECEIVER_EMAIL
    password = conf.EMAIL_PWD

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

def generate_password_change_email(RECEIVER_EMAIL):
    subject = "URGENT: Password Change"
    body ="\nHi User,\n\n Your password changed successfully "
    sender_email = conf.EMAIL_ID
    receiver_email = RECEIVER_EMAIL
    password = conf.EMAIL_PWD

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    context = ssl.create_default_context()
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

def update_password(email,password,database):
    query = "UPDATE USERS SET PASSWORD ='" + str(password) + "' where EMAIL='" + str(email) + "'"
    database.execute(query)