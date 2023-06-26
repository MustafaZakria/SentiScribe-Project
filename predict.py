import models.model as my_model
import data_preprocessing

# Load the model and vectorizer
model = my_model.load_model()
vectorizer = my_model.load_vectorizer()


def labels_to_string(polarity):
    if polarity == 1:
        return 'Positive'
    elif polarity == -1:
        return 'Negative'

def sentiment_predict(df_reviews):
    temp_df = df_reviews.copy()
    temp_df["cleaned_reviews"] = temp_df["Reviews"].apply(data_preprocessing.preprocessing)
    temp_df = temp_df[temp_df['cleaned_reviews'].str.len() > 0]

    sequences = vectorizer.transform(temp_df['cleaned_reviews'])

    # predict the sentiment by setting the probability threshold to 0.50
    score = model.predict(sequences)
    temp_df["Sentiment"] = score
    temp_df["Sentiment"] = temp_df["Sentiment"].apply(
        lambda x: "Positive" if x == 1 else "Negative"
    )
    temp_df = temp_df.drop(['cleaned_reviews'], axis=1)
    return temp_df

def sentiment_predict_user_input(user_review):
    cleaned_text = data_preprocessing.preprocessing(user_review)
    sequences = vectorizer.transform([cleaned_text])
    score = model.predict(sequences)
    sentiment_label = labels_to_string(score)
    return sentiment_label

