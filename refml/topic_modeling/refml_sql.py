from refml.topic_modeling.preprocess import stem_and_tokenize
from refml.topic_modeling.model import refml_model
import pandas as pd

def runrefml(input, n_topics, n_top_words, n_dimensions, perplexity):
    df['Text_Processed'] = input.apply(stem_and_tokenize)
    return refml_model(df.Text_Processed, n_topics, n_top_words, n_dimensions, perplexity)

def refml_for_sql(sql_in, input_column, n_topics, n_top_words, n_dimensions, perplexity):
    input = pd.from_sql(sql_in)
    output = runrefml(input.input_column, n_topics, n_top_words, n_dimensions, perplexity)
    return pd.to_sql(output)