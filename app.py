from refml.topic_modeling.preprocess import stem_and_tokenize
from refml.topic_modeling.model import refml_model, visualize
import streamlit as st
import pandas as pd
import base64

st.markdown('# REFML Prototype')
st.sidebar.markdown('## Modeling options:')

n_topics = st.sidebar.slider('Number of topics: ', 5, 50, 20, step = 1)

st.sidebar.markdown('## Visualization options:')

n_dimensions = st.sidebar.radio('2 or 3 dimensional visualization?', [2, 3])
n_top_words = st.sidebar.slider('Number of top words:', 3, 15, 5, step = 5)
perplexity = st.sidebar.slider('TSNE perplexity:', 5, 50, 20, step = 1)

@st.cache
def load_and_process():
    ## load data:
    df = pd.read_excel('Night Shift Work and Light at Night_ Human cancer and biomonitoring studies (2018)-refs.xlsx')
    df['Text'] = df['Title'] + " " + df['Abstract'].astype(str)

    ## apply text preprocessing to text input field
    df['Text_Processed'] = df['Text'].apply(stem_and_tokenize)
    return df

@st.cache
def model():
    ## run refml topic clustering model
    reduced = refml_model(df.Text_Processed, n_topics, n_top_words, n_dimensions, perplexity)

    ## join model results to input dataframe
    export = reduced.join(df)
    return export

@st.cache
def visual():
    return visualize(export, n_dimensions = 2)

df = load_and_process()
export = model()
fig = visual()

st.markdown('## TSNE Visualization:')
st.markdown('Each cluster is assigned a color. Hover over the plot to explore the results.')
st.plotly_chart(fig)

st.markdown('## Data output:')
st.write(export)