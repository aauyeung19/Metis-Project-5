"""
Author: Andrew

Streamlit App For Classifying articles and blogs to their respective types of articles...
"""
import streamlit as st
from gensim.models.doc2vec import Doc2Vec
import pandas as pd
from cleaning import prep_doc2vec
from collections import Counter 
model = Doc2Vec.load('../models/d2v_v5.model')

@st.cache
def load_tables():
    """
    Cache immutable tables to save time on loading
    """
    return pd.read_csv('../src/streamlit_src.csv', index_col=0)

# MVP: User c/p text--> Model infers vector --> Model suggests 5 most similar documents with their titles and topics 
def show_similar(model, text):
    """
    Infers the document vector of the cleaned text and returns a list with the n_to_show most similar article_ids
    args:
        model (mdl): Gensim Doc2vec model
        text (str): cleaned string of articles
        n_to_show (int): number of articles to show
    returns:
        similar_articles (list): list of article ids as strings
    """
    new_vec = model.infer_vector(text.split())
    similar_articles = [int(x[0]) for x in model.docvecs.most_similar([new_vec])]
    return similar_articles

@st.cache(allow_output_mutation=True)
def cache_raw_text():
    return []

@st.cache(allow_output_mutation=True)
def cache_similar_articles():
    return[]

if __name__ == "__main__":
    st.title("What is THIS data scientist talking about?")
    st.write("This app parses a document and suggests possible Data Science tags.")
    st.write("Currently tags are high level tags of what the article may talk about.  Check back later for more updates!")
    labels = load_tables()
    # load caches
    text_cache = cache_raw_text()
    similar_cache = cache_similar_articles()
    cluster_labels = [
        'Metrics and ML Algorithms',
        'Neural Networks and Linear Algebra', 
        'Stocks and Statistics',
        'Natural Language Processing',
        'Exploratory Data Analysis',
        'AI and Data Analytics',
        'Business and Interviews',
        'Images and Object Detection',
        'Data Science Careers',
        'Big Data and Databases'
    ]

    text = st.text_area("Copy and paste your article here.")
    if len(text_cache) == 0:
        text_cache.append(prep_doc2vec(text))
    elif text_cache[-1] == text:
        pass
    else:
        text_cache.append(prep_doc2vec(text))
    text = text_cache[-1]
    
    if len(text_cache) == len(similar_cache):
        similar_articles = similar_cache[-1]
    else:
        similar_articles = show_similar(model, text)
    
    cluster_num = [labels.loc[a].cluster for a in similar_articles]
    tags = Counter(cluster_labels[i] for i in cluster_num)
    tags = sorted(tags, key=lambda x:tags[x], reverse=True)
    tags = ', '.join(tags)
    st.write(f"Suggested Tag(s) are: {tags}")

    st.write("Here are some similar articles to check out:")
    n_to_show = st.slider(label="Number of Similar Articles:", min_value=1, max_value=10, step=1)
    for article in similar_articles[:n_to_show]:
        title = labels.loc[article].title
        link = labels.loc[article].link
        f"[{title}]({link})" # streamlit magic function for writing markdown
        st.text(f"Topic: {cluster_labels[labels.loc[article].cluster]}")
