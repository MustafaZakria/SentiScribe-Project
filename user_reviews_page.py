import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import scrapping.reviews_scrapping as scrap
import predict
import dataset.load_restaurants as rest
import visualization

restaurants_names = rest.load_restaurant_names()


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def choose_from_restaurants():
    selected_option = st.selectbox('Select an option', restaurants_names)
    st.write('You selected:', selected_option)

    st.write('It may take sometime, please be patient:)')
    if st.button('Scrap and Predict!'):
        st.write('Scrapping....')
        df_scrapped = scrap.scrap(selected_option)
        df_predicted = predict.sentiment_predict(df_scrapped)
        # st.dataframe(df_predicted.style.applymap(color_sentiment, subset=['Sentiment']))
        visualization.make_dashboard(df_predicted)
    # st.divider()


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

    # st.divider()


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

    page_bg_img = """
    <style>
    .stApp {
    background-size: cover;
    background-repeat: no-repeat;
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");    
    
    }
    
    [data-testid="stVerticalBlock"] {
    background-color: rgba(239, 239, 240);
    padding: 20px;
    }
    
    
    [data-testid="stHorizontalBlock"] {
    padding: 0px
    }

    [data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
    }
    
    [data-baseweb="select"] {
    width: 300px;
    }
    
    [data-baseweb="input"] {
    width: 600px;
    }
    
    [data-baseweb="tab"] {
    background-color: rgba(0, 0, 0, 0);
    }
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

    # st.subheader("Zeko's Kitchen")

    menu = ["Choose From Restaurants", "Upload a CSV", "Write a Single Review"]
    # option = st.selectbox(
    #     'Choose a way to provide your reviews!',
    #     menu)
    #
    # st.write("<br>", unsafe_allow_html=True)
    #
    # if option == "Choose From Restaurants":
    #     choose_from_restaurants()
    # elif option == "Upload a CSV":
    #     predict_a_csv()
    # elif option == "Write a Single Review":
    #     predict_single_review()

    option = st.radio('Choose a way to provide your reviews!', menu)

    st.write("<br>", unsafe_allow_html=True)

    if option == "Choose From Restaurants":
        choose_from_restaurants()
    elif option == "Upload a CSV":
        predict_a_csv()
    elif option == "Write a Single Review":
        predict_single_review()
