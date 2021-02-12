from sklearn.decomposition import NMF
from sklearn.manifold import TSNE
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

def get_nmf_topics(model, n_top_words, n_topics, vectorizer):
    
    #the word ids obtained need to be reverse-mapped to the words so we can print the topic names.
    feat_names = vectorizer.get_feature_names()
    
    word_dict = {}
    for i in range(n_topics):
        
        #for each topic, obtain the largest values, and add the words they map to into the dictionary.
        words_ids = model.components_[i].argsort()[:-n_top_words - 1:-1]
        words = [feat_names[key] for key in words_ids]
        wordstring = str('')
        for word in words:
            wordstring += word + ' '
        word_dict[i] = wordstring
    
    return pd.Series(word_dict, name = 'top words')

def refml_nmf(preprocessed_words, n_topics, n_top_words):
    
    #vectorize preprocessed text
    vectorizer = CountVectorizer(analyzer='word')#, max_features=5000)
    x_counts = vectorizer.fit_transform(preprocessed_words)

    #Tfidf encoding
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(x_counts)

    #NMF topic modeling
    model = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(X_train_tfidf.T)

    #Match categories to original titles
    topic_values = model.fit_transform(X_train_tfidf)
    clustered = pd.DataFrame(topic_values.argmax(axis=1), columns = ['category'])

    #get top words
    top_words = get_nmf_topics(model, n_top_words, n_topics, vectorizer)

    export = pd.merge(top_words, clustered, right_on='category', left_index=True)

    return export

def refml_nmf_tsne(preprocessed_words, n_topics, n_top_words, n_dimensions, perplexity):
    
    #vectorize preprocessed text
    vectorizer = CountVectorizer(analyzer='word')#, max_features=5000)
    x_counts = vectorizer.fit_transform(preprocessed_words)

    #Tfidf encoding
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(x_counts)

    #NMF topic modeling
    model = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(X_train_tfidf.T)

    #Match categories to original titles
    topic_values = model.fit_transform(X_train_tfidf)
    clustered = pd.DataFrame(topic_values.argmax(axis=1), columns = ['category'])

    #get top words
    top_words = get_nmf_topics(model, n_top_words, n_topics, vectorizer)

    #dimensionality reduction
    nmf = model.fit(X_train_tfidf.T)
    nmf_embedded = TSNE(n_components=n_dimensions, perplexity=perplexity).fit_transform(nmf.components_.T)

    #join nmf and tsne results and clean up column names
    export = pd.merge(top_words, clustered, right_on='category', left_index=True).join(pd.DataFrame(nmf_embedded))
    if n_dimensions == 2:
        export['dim_2'] = np.nan
    export.columns = ['top_words', 'category', 'dim_0', 'dim_1', 'dim_2']

    return export

def visualize(tsne_reduced_df, n_dimensions):
    
    if n_dimensions == 2:
        fig = px.scatter(tsne_reduced_df, x= 'dim_0', y= 'dim_1', 
                    color = 'category', color_continuous_scale = 'Rainbow',
                   hover_data = ['top_words', 'Title'])
        fig.update_traces(marker = dict(size=5))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        return fig
    
    elif n_dimensions == 3:
        fig = px.scatter_3d(tsne_reduced_df, x= 'dim_0', y= 'dim_1', z= 'dim_2', 
                    color = 'category', color_continuous_scale = 'Rainbow',
                   hover_data = ['top_words', 'Title'])
        fig.update_traces(marker = dict(size=3))
        return fig
    
    else:
        print('dimensions must be 2 or 3')