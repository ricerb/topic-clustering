from sklearn.decomposition import NMF
from sklearn.manifold import TSNE
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def get_nmf_topics(vectorizer, model, n_top_words):
    
    #the word ids obtained need to be reverse-mapped to the words so we can print the topic names.
    feat_names = vectorizer.get_feature_names()
    
    word_dict = {}
    for i in range(n_top_words):
        
        #for each topic, obtain the largest values, and add the words they map to into the dictionary.
        words_ids = model.components_[i].argsort()[:-n_top_words - 1:-1]
        words = [feat_names[key] for key in words_ids]
        wordstring = str("")
        for word in words:
            wordstring += word + " "
        word_dict[i] = wordstring
    
    return pd.Series(word_dict)

def refml_model(preprocessed_words, n_topics, n_top_words):

    #vectorize strings
    vectorizer = CountVectorizer(analyzer='word', max_features=5000)
    x_counts = vectorizer.fit_transform(preprocessed_words)

    #tfidf encode vectorized strings
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(x_counts)

    #initialize nmf model
    model = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd')

    #fit model to data
    nmf = model.fit(X_train_tfidf.T)
    
    # get top words for each cluster
    top_words = pd.DataFrame(get_nmf_topics(vectorizer = vectorizer, model = nmf, n_top_words = n_top_words), columns = ['top words'])

    # label clusters
    topic_values = pd.DataFrame(model.fit_transform(X_train_tfidf).argmax(axis=1), columns = ['category'])

    clusterdf = pd.merge(top_words, topic_values, right_on='category', left_index=True)

    return nmf, clusterdf

def tsne_reduce(model_output, n_dimensions, perplexity):
    
    nmf_embedded = TSNE(n_components=n_dimensions, perplexity=perplexity).fit_transform(model_output.components_.T)

    return pd.DataFrame(nmf_embedded)

def visualize(tsne_reduced_df, n_dimensions):
    
    if n_dimensions == 2:
        fig = px.scatter(tsne_reduced_df, x= 0, y= 1, 
                    color = 'category', color_continuous_scale = 'Rainbow',
                   hover_data = ['top words', 'Text'])
        fig.update_traces(marker = dict(size=5))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        return fig
    
    elif n_dimensions == 3:
        fig = px.scatter_3d(tsne_reduced_df, x= 0, y= 1, z= 2, 
                    color = 'category', color_continuous_scale = 'Rainbow',
                   hover_data = ['top words', 'Text'])
        fig.update_traces(marker = dict(size=3))
        return fig
    
    else:
        print('dimensions must be 2 or 3')