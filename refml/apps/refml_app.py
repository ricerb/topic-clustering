from refml.topic_modeling.preprocess import stem_and_tokenize
from refml.topic_modeling.model import refml_nmf_tsne, visualize
import streamlit as st
import pandas as pd
import os

st.markdown('# REFML Prototype')

def upload():
    file = st.sidebar.file_uploader('Upload File (csv or excel) and select a column to run refml on.', type = ['csv', 'xls', 'xlsx'])
    if file:
        try:
            df = pd.read_csv(file)
        except:
            df = pd.read_excel(file)
        else:
            st.write('input not read into dataframe')
        text = st.sidebar.selectbox('Pick the text input column:', df.columns.tolist())
    else:
        df = pd.DataFrame()
        text = ''
    return df, text


def options():
    st.sidebar.markdown('## Modeling options:')
    data = st.sidebar.radio('Which test dataset? (Night Work and Ozone options run refml on titles and abstracts from preloaded literature search results.)', ['Night Work', 'Ozone', 'Uploaded File'])
    n_topics = st.sidebar.slider('Number of topics: ', 5, 50, 20, step = 1)

    st.sidebar.markdown('## Visualization options:')
    n_dimensions = st.sidebar.radio('2 or 3 dimensional visualization?', [2, 3])
    n_top_words = st.sidebar.slider('Number of top words:', 3, 15, 5, step = 5)
    perplexity = st.sidebar.slider('TSNE perplexity:', 5, 50, 20, step = 1)
    start = st.sidebar.button('Run refml')
    return data, n_topics, n_dimensions, n_top_words, perplexity, start


@st.cache()
def load_and_process(data, df, text):
    if data == 'Night Work':
        ## load data:
        df = pd.read_excel('Night Shift Work and Light at Night_ Human cancer and biomonitoring studies (2018)-refs.xlsx')
        df['Text'] = df['Title'] + " " + df['Abstract'].astype(str)

        ## apply text preprocessing to text input field
        df['Text_Processed'] = df['Text'].apply(stem_and_tokenize)

    elif data == 'Ozone':
        df = pd.read_pickle('ozone_data_fromhero.pkl').iloc[:10000,:]
        df['Text'] = df['TITLE'] + " " + df['ABSTRACT'].astype(str)
        df['Title'] = df['TITLE']
        df['Text_Processed'] = df['Text'].apply(stem_and_tokenize)

    elif data == 'Uploaded File':
        df['Text_Processed'] = df[text].apply(stem_and_tokenize)
        df['Title'] = df[text].astype(str).str[:30]
    return df

@st.cache
def model(df):
    ## run refml topic clustering model
    reduced = refml_nmf_tsne(df.Text_Processed, n_topics, n_top_words, n_dimensions, perplexity)

    ## join model results to input dataframe
    export = reduced.join(df)
    return export

@st.cache
def visual(export):
    return visualize(export, n_dimensions = n_dimensions)

df, text = upload()
data, n_topics, n_dimensions, n_top_words, perplexity, start = options()
if start:
    df = load_and_process(data, df, text)

    export = model(df)
    fig = visual(export)

    st.markdown('## TSNE Visualization:')
    st.markdown('Each cluster is assigned a color. Hover over the plot to explore the results. View in fullscreen for best presentation.')
    st.plotly_chart(fig)

    st.markdown('## Data output:')
    st.write(export)

    ## file download hack
    import base64
    csv = export.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="export.csv" >Download Output CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)