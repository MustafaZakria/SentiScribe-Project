import pandas as pd
import numpy as np
import streamlit as st
st.set_page_config(page_title="SentiScribe", page_icon='https://cdn-icons-png.flaticon.com/512/8637/8637099.png')
import matplotlib.pyplot as plt
import plotly.express as px
import scrapping.reviews_scrapping as scrap
import predict
import dataset.load_restaurants as rest

restaurants_names = rest.load_restaurant_names()

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def color_sentiment(val):
    color = 'green' if val == 'Positive' else 'red'
    return f'background-color: {color}; color: white'

def choose_from_restaurants():
    selected_option = st.selectbox('Select an option', restaurants_names)
    st.write('You selected:', selected_option)

    st.write('It may take sometime, please be patient:)')
    if st.button('Scrap and Predict!'):
        st.write('Scrapping....')
        df_scrapped = scrap.scrap(selected_option)
        df_predicted = predict.sentiment_predict(df_scrapped)
        df_predicted = df_predicted.style.applymap(color_sentiment, subset=['Sentiment'])
        st.dataframe(df_predicted)
    st.divider()

def predict_a_csv():
    st.subheader("Upload your reviews!")
    st.markdown("**Hint: Please name the reviews column as :red['Reviews']**")
    with st.expander('Analyze CSV'):
        upl = st.file_uploader('Upload file')
    if upl:
        data = pd.read_csv(upl)
        flag = False
        for column in data.columns:
            if column == "Reviews":
                flag = True
                break
        if flag:
            dataset = predict.sentiment_predict(data)
            new_df = pd.DataFrame({'Reviews': dataset['Reviews'], 'Sentiment': dataset['Sentiment']})
            st.write(new_df.head(5))

            csv_file = convert_df(dataset)

            st.download_button(
                label="Download data as CSV",
                data=csv_file,
                file_name='labeled_data.csv',
                mime='text/csv',
            )
        else:
            st.text("Your CSV Does not Contain Column Reviews")

    st.divider()

def predict_single_review():
    st.subheader("User Input Review Analysis")
    st.text("""
        Analyzing reviews given by the user and find sentiments
        within it (positive or negative).
        """)
    st.write("")
    user_review = st.text_input('Enter Review', placeholder='Write your review...', key="")
    if st.button('Predict'):
        if user_review:
            sentiment_label = predict.sentiment_predict_user_input(user_review)
            if sentiment_label == "Positive":
                st.write(f"**:green[{sentiment_label}]**")
            else:
                st.write(f"**:red[{sentiment_label}]**")


def main_menu():
    st.title("Sentiment Analysis 😊😡")
    st.markdown('---')
    st.subheader("Zeko's Kitchen")
    menu = ["Choose From Restaurants", "Upload a CSV", "Write a Single Review"]
    option = st.selectbox(
        'Choose a way to provide your reviews!',
        menu)
    if option == "Choose From Restaurants":
        choose_from_restaurants()
    elif option == "Upload a CSV":
        predict_a_csv()
    elif option == "Write a Single Review":
        predict_single_review()



