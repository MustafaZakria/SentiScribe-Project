import pickle
import streamlit as st

@st.cache_data
def load_model():
    with open('models/svm_model_1.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data
def load_vectorizer():
    with open('models/tfidf_vectorizer.pkl', 'rb') as f:
        return pickle.load(f)