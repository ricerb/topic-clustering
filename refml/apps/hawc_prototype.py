from refml.topic_modeling.preprocess import stem_and_tokenize
from refml.topic_modeling.model import refml_nmf_tsne, visualize
import streamlit as st
import pandas as pd
import os

path = os.path.dirname(__file__)
os.chdir(path)

st.markdown('# REFML Prototype for HAWC')

## run model and cache results
@st.cache()
def do_it():
    df = pd.read_pickle('Ozone_included_refs.pkl')
    df['Text_Processed'] = df['Title'].apply(stem_and_tokenize)
    output = refml_nmf_tsne(df.Text_Processed, n_topics = 20, n_top_words = 10, n_dimensions = 2, perplexity = 30)
    return df.join(output)

model_results = do_it()

## create figure
fig = visualize(model_results, n_dimensions = 2)

## display plot
st.plotly_chart(fig)

st.markdown(
    '''This is a TSNE visualization of a NMF topic clustering method applied to the references in this project.
References are colored by topic. The title of the reference and the most important words forming each cluster
are displayed when you hover your mouse over the plot.'''
)