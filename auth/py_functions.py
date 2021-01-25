import pandas as pd

def check_user_details(username,password,cnxn):
    query = 'select * from USER_CREDS where email='+"'"+str(username)+"'"+' and PASSWORD='+"'"+str(password)+"'"
    df= pd.read_sql(query,cnxn)
    return df.shape[0]