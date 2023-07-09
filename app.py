import streamlit as st
st.set_page_config(page_title="SentiScribe", page_icon='https://i.imgur.com/eP2jxYt.png', layout="wide")
from user_reviews_page import main_menu

if __name__ == "__main__":
    main_menu()