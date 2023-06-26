import streamlit as st
import ast

@st.cache_data
def load_dictionary_from_file():
    with open("dataset/restaurants.txt", 'r') as file:
        data = file.read()
    return ast.literal_eval(data)

@st.cache_data
def load_restaurant_names():
    
    restaurants = load_dictionary_from_file()

    restaurant_names = []

    for _, value in restaurants.items():
        restaurant_names.append(value['name'])
    return restaurant_names

