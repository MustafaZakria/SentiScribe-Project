import pickle
import streamlit as st
from transformers import pipeline


@st.cache_data
def load_stopwords():
    stopwords_path = 'models/arabic_stopwords.txt'
    stop_words = set()
    with open(stopwords_path, 'r', encoding='utf-8') as file:
        content = file.read()
        words = content.split('\n')
        stop_words = set(words)
    return stop_words

@st.cache_data
def load_model():
    #with open('models/svm_model_1.pkl', 'rb') as f:
    #    return pickle.load(f)
    pipe = pipeline("sentiment-analysis", model="models/arabert", return_all_scores=False)
    return pipe


@st.cache_data
def load_vectorizer():
    with open('models/tfidf_vectorizer.pkl', 'rb') as f:
        return pickle.load(f)