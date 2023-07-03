import pandas as pd
import streamlit as st
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

    number_of_reviews = st.slider("How many reviews needs to be scrapped?\n\n:red[Note: the restaurant's reviews may be less than the specified.]", min_value=20, max_value=1000, value=20, step=20)

    if st.button('Scrap and Predict!'):
        st.write('It may take sometime, please be patient:)')
        st.write('Scrapping....')
        df_scrapped = scrap.scrap(selected_option, number_of_reviews)

        if df_scrapped is None:
            text = f"{selected_option} has no reviews"
            centered_text = f"<p style='text-align: center; font-size: large; font-weight: bold; color: red'>{text}</p>"
            st.markdown(centered_text, unsafe_allow_html=True)
        else:
            df_predicted = predict.sentiment_predict(df_scrapped)
            visualization.make_dashboard(df_predicted, src='choose_from_restaurants')

            st.divider()

def predict_a_csv():
    st.subheader("Upload your reviews!", anchor=False)
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
            new_df = pd.DataFrame({'Reviews': dataset['Reviews'], 'Sentiment': dataset['Sentiment'], 'Score': dataset['Score']})
            st.subheader("Predicted Sentiment", anchor=False)
            csv_file = convert_df(new_df)

            visualization.make_dashboard(dataset, src='csv')

            st.download_button(
                label="Download data as CSV",
                data=csv_file,
                file_name='labeled_data.csv',
                mime='text/csv',
            )

        else:
            st.text("Your CSV doesn't contain a column named 'Reviews'")

        st.divider()

def predict_single_review():
    st.subheader("User Input Review Analysis", anchor=False)
    st.text("""
        Analyzing reviews given by the user and find sentiments
        within it (positive or negative).
        """)
    st.write("")
    user_review = st.text_input('Enter Review', placeholder='Write your review...')
    
    if st.button('Predict'):
        if user_review:
            sentiment_label, score = predict.sentiment_predict_user_input(user_review)
            
            if sentiment_label == "Positive":
                st.write(f"Polarity: **:green[{sentiment_label}]**")
                st.write(f"Score of Positivity: **:green[{score}]**")
            else:
                st.write(f"Polarity: **:red[{sentiment_label}]**")
                st.write(f"Score of Negativity: **:red[{score}]**")


def main_menu():
    st.markdown(
        """
        <div style='display: flex; align-items: center;'>
            <img src='icons/FilledDark.png' alt='icon' width='50px' style='margin-right: 10px;'> 
            <h1 style='font-size: 50px;'>SentiScribe </h1> 
        </div>

        """,
        unsafe_allow_html=True
    )
    st.markdown('---')
    st.subheader("Sentiment Analysis 😊😡", anchor=False)
    menu = ["Choose From Restaurants", "Upload a CSV", "Write a Single Review"]
    option = st.radio('Choose a way to provide your reviews!', menu)

    st.write("<br>", unsafe_allow_html=True)

    if option == "Choose From Restaurants":
        choose_from_restaurants()
    elif option == "Upload a CSV":
        predict_a_csv()
    elif option == "Write a Single Review":
        predict_single_review()