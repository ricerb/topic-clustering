from refml.topic_modeling.preprocess import stem_and_tokenize
from refml.topic_modeling.model import refml_nmf_tsne
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, String, Float
import cx_Oracle

def hero_to_df(Userid, Password, Host, Port, SID, query):
    dsn_tns = cx_Oracle.makedsn(host=Host, port=Port, sid=SID)
    conn = cx_Oracle.connect(user=Userid, password=Password, dsn=dsn_tns)

    return pd.read_sql_query(query, conn)

def refml_to_sql(df, input_column, n_topics, n_top_words, n_dimensions, perplexity):
    df['Text_Processed'] = df[input_column].apply(stem_and_tokenize)
    export = refml_nmf_tsne(df.Text_Processed, n_topics, n_top_words, n_dimensions, perplexity)

    # Create in memory sqlite3 database
    engine = create_engine('sqlite://', echo=False)
    return export.to_sql('refml_export',
            engine,
            if_exists='replace', 
            index=False,  ##not sure if I need this to be true or not??
            dtype={'top_words': String,
                'category': Integer,
                '0': Float,
                '1': Float})

def hero_titles_to_refml_input(usageid, Userid, Password):
    #query heroprd using Byron's login information
    Host = "herodb.rtpnc.epa.gov"
    Port = "1521"
    SID = "heroprd"

    query = f'''select reference_id, year, title 
    from tbl_reference 
    where sdelete = 'No' 
    and reference_id in
    (select reference_id from tbl_reference_usage where usage_id = {usageid} and isdeleted = 0)'''

    df = hero_to_df(Userid, Password, Host, Port, SID, query)
    df['Text'] = df.TITLE.astype(str)
    return df

def hero_titles_abstracts_to_refml_input(usageid):
    #query heroprd using Byron's login information
    Userid = "rrice"
    Password = "Temp02122020" 
    Host = "herodb.rtpnc.epa.gov"
    Port = "1521"
    SID = "heroprd"

    query = f'''select reference_id, year, title, abstract 
    from tbl_reference 
    where sdelete = 'No' 
    and reference_id in
    (select reference_id from tbl_reference_usage where usage_id = {usageid} and isdeleted = 0)'''
    
    df = hero_to_df(Userid, Password, Host, Port, SID, query)
    df.ABSTRACT = df.ABSTRACT.astype(str)
    df.TITLE = df.TITLE.astype(str)
    df['Text'] = df['TITLE'] + str(' ') + df['ABSTRACT']
    return df