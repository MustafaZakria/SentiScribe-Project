import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
import arabic_reshaper
from bidi.algorithm import get_display
# To get stop_words
from models.model import load_stopwords
# for visualization
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import altair as alt
import pandas as pd

pd.set_option('display.max_colwidth', None)

@st.cache_data
def plot_sentiment(df_reviews):
    # count the number tweets based on the sentiment
    sentiment_count = df_reviews["Sentiment"].value_counts()

    # plot the sentiment distribution in a pie chart
    fig = px.pie(
        values=sentiment_count.values,
        names=sentiment_count.index,
        hole=0.3,
        title="<b>Sentiment Distribution</b>",
        color=sentiment_count.index,
        # set the color of positive to blue and negative to orange
        color_discrete_map={"Positive": "green", "Negative": "red"},
    )
    fig.update_traces(
        textposition="inside",
        texttemplate="%{label}<br>%{value} (%{percent})",
        hovertemplate="<b>%{label}</b><br>Percentage=%{percent}<br>Count=%{value}",
    )
    fig.update_layout(showlegend=False)
    return fig

@st.cache_data
def plot_wordcloud(df_reviews):
    # generate custom colormap
    # cmap = mpl.cm.get_cmap(colormap)(np.linspace(0, 1, 20))
    # cmap = mpl.colors.ListedColormap(cmap[10:15])
     # combine all the preprocessed tweets into a single string
    text = " ".join(df_reviews["cleaned_reviews"])
    reshaped_text = arabic_reshaper.reshape(text)
    reshaped_text = get_display(reshaped_text)

    wc = WordCloud(
        background_color="white",
        font_path="fonts/NotoNaskhArabic-Regular.ttf",
        max_words=90,
        random_state=42,
        collocations=False,
        min_word_length=2,
        max_font_size=200,
    ).generate(reshaped_text)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Wordcloud", fontdict={"fontsize": 16}, fontweight="heavy", pad=20, y=1.0)
    return fig

@st.cache_data
def dashboard(df_reviews, bar_color, wc_color):
    # make 3 columns for the first row of the dashboard
    df_reviews['cleaned_reviews'] = df_reviews['cleaned_reviews'].apply(remove_stop_words)
    col1, col2, col3 = st.columns(3)
    with col1:
        # plot the sentiment distribution
        sentiment_plot = plot_sentiment(df_reviews)
        sentiment_plot.update_layout(height=350, title_x=0.5)
        st.plotly_chart(sentiment_plot, theme=None, use_container_width=True)

        try:
            with col2:
                # plot the top 10 occuring bigrams
                top_unigram = get_top_n_gram(df_reviews, ngram_range=(2, 2), n=10)
                unigram_plot = plot_n_gram(
                    top_unigram, title="Top 10 Occurring Words", color=bar_color
                )
                unigram_plot.update_layout(height=350)
                st.plotly_chart(unigram_plot, theme=None, use_container_width=True)

            with col3:
                # plot the top 10 occuring trigrams
                top_bigram = get_top_n_gram(df_reviews, ngram_range=(3, 3), n=10)
                bigram_plot = plot_n_gram(
                    top_bigram, title="Top 10 Occurring Words", color=bar_color
                )
                bigram_plot.update_layout(height=350)
                st.plotly_chart(bigram_plot, theme=None, use_container_width=True)
        except:
            pass

    # make 2 columns for the second row of the dashboard
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        # function to color the sentiment column
        def sentiment_color(sentiment):
            if sentiment == "Positive":
                return "background-color: green; color: white"
            else:
                return "background-color: red; color: white"

        # show the dataframe containing the tweets and their sentiment
        # pd.set_option('display.width', 1000)
        df_styled = df_reviews[["Reviews", "Sentiment", 'Score']].style.applymap(sentiment_color, subset=['Sentiment'])
        st.dataframe(df_styled)
        

    with col2:
        # plot the wordcloud
        st.pyplot(plot_wordcloud(df_reviews))

stop_words = load_stopwords()

def remove_stop_words(text):
    return ' '.join([word for word in text.split() if word not in stop_words])

def get_top_n_gram(df_reviews, ngram_range, n=10):

    # load the corpus and vectorizer
    corpus = df_reviews["cleaned_reviews"]
    vectorizer = CountVectorizer(
        analyzer="word", ngram_range=ngram_range
    )

    # use the vectorizer to count the n-grams frequencies
    X = vectorizer.fit_transform(corpus.astype(str).values)
    words = vectorizer.get_feature_names_out()
    words_count = np.ravel(X.sum(axis=0))

    # store the results in a dataframe
    df = pd.DataFrame(zip(words, words_count))
    df.columns = ["words", "counts"]
    df = df.sort_values(by="counts", ascending=False).head(n)
    df["words"] = df["words"].str.title()
    return df

def plot_n_gram(n_gram_df, title, color="#54A24B"):
    # plot the top n-grams frequencies in a bar chart
    fig = px.bar(
        x=n_gram_df.counts,
        y=n_gram_df.words,
        title="<b>{}</b>".format(title),
        text_auto=True,
    )
    fig.update_layout(plot_bgcolor="white")
    fig.update_xaxes(title=None)
    fig.update_yaxes(autorange="reversed", title=None)
    fig.update_traces(hovertemplate="<b>%{y}</b><br>Count=%{x}", marker_color=color)
    return fig

@st.cache_data
def sentiment_over_time(df):
    _, col2, _ = st.columns(3)
    with col2:
        df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
        counts = {}

        # Iterate through each data point
        for _, data in df.iterrows():
            sentiment = data['Sentiment']
            date = data['Date']

            # Increment the corresponding counter based on sentiment
            if date not in counts:
                counts[date] = {'Positive': 0, 'Negative': 0}

            counts[date][sentiment] += 1

        dates = list(counts.keys())
        positive_counts = []
        negative_counts = []
        for date in counts:
            positive_counts.append(counts[date]['Positive'])
            negative_counts.append(counts[date]['Negative'])

        data = {
            'Date': dates,
            'Positive': positive_counts,
            'Negative': negative_counts
        }

        # Convert data to DataFrame
        df = pd.DataFrame(data)
        color_scale = alt.Scale(domain=['Positive', 'Negative'],
                                range=['green', 'red'])
        # Create the Altair chart
        chart = alt.Chart(df, title='Sentiment Over Time').mark_line().encode(
            x='Date:T',
            y='Counts:Q',
            color=alt.Color('sentiment:N', scale=color_scale)
        ).transform_fold(
            fold=['Positive', 'Negative'],
            as_=['sentiment', 'Counts']
        )

        chart = chart.properties(
            width=600,  # Set the width of the chart in pixels
            height=400  # Set the height of the chart in pixels
        )

        st.altair_chart(chart)


def make_dashboard(df_reviews, src):
    tab1, tab2, tab3 = st.tabs(["All", "Positive 😊", "Negative ☹️"])
    # Both positive and negative reviews tab
    with tab1:
        dashboard(df_reviews, bar_color="#1F77B4", wc_color="Blues")
        if src == 'choose_from_restaurants':
            sentiment_over_time(df_reviews)
    with tab2:
        # Positive reviews tab
        df_pos = df_reviews[df_reviews['Sentiment'] == 'Positive']
        st.write("No positive reviews") if df_pos.empty else dashboard(df_pos, bar_color="green")

    with tab3:
        # Negative reviews tab
        df_neg = df_reviews[df_reviews['Sentiment'] == 'Negative']
        st.write("No negative reviews") if df_neg.empty else dashboard(df_neg, bar_color="red")