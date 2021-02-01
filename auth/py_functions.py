import pandas.io.sql as psql

def fetch_data(search,engine):
    query_cols = 'select top 1+ from DATABASE-1'
    df=psql.read_sql(query_cols,engine)
    col_list=(','.join(df.columns))
    print(col_list)

    query = 'SELECT TOP 10* FROM DATABASE-1'\
         "where lower(concat("+col_list+") like '%"+search+"%'"

    print(query)
    df = psql.read_sql(query,engine)
    return df
