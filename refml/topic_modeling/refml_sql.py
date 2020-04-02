import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, String, Float
import cx_Oracle

def get_db_conn(Userid, Password, Host, Port, SID): # use cx_oracle module to establish connection to database

    dsn_tns = cx_Oracle.makedsn(host=Host, port=Port, sid=SID)
    return cx_Oracle.connect(user=Userid, password=Password, dsn=dsn_tns)

def refml_nmf_tsne_to_db(df, ref_id_col, engine): # takes model output pandas dataframe and engine as inputs and returns in-memory sqlite database
    df['ref_id'] = df[ref_id_col]
    return df.to_sql('refml_nmf_tsne_export',
            engine,
            if_exists='replace', 
            index=False,  ##not sure if I need this to be true or not??
            dtype={'ref_id': Integer,
                'top_words': String,
                'category': Integer,
                'dim_0': Float,
                'dim_1': Float,
                'dim_2': Float})

def hero_titles_to_refml_input(usageid, conn): # input hero tag usage id and database connection, returns pandas dataframe of HERO IDs, year, and title

    query = f'''select reference_id, year, title 
    from tbl_reference 
    where sdelete = 'No' 
    and reference_id in
    (select reference_id from tbl_reference_usage where usage_id = {usageid} and isdeleted = 0)'''

    df = pd.read_sql(query, conn)
    df['TITLE'] = df.TITLE.astype(str)

    return df

def hero_titles_abstracts_to_refml_input(usageid, conn): # input hero tag usage id and database connection, returns pandas dataframe of HERO IDs, year, title, and abstract

    query = f'''select reference_id, year, title, abstract 
    from tbl_reference 
    where sdelete = 'No' 
    and reference_id in
    (select reference_id from tbl_reference_usage where usage_id = {usageid} and isdeleted = 0)'''

    df = pd.read_sql(query, conn)

    df['Title and Abstract'] = df['TITLE'].astype(str) + str(' ') + df['ABSTRACT'].astype(str)
    return df