import re

def remove_diacritics(text):
    arabic_diacritics = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    text = re.sub(arabic_diacritics, '', str(text))
    return text

def remove_arabic_digits(text):
    return re.sub("[\u0660-\u0669]+", '', text)

def preprocessing(text):

    # Using regex to remove all non-Arabic letters, digits, punctuation marks, and emojis
    text = re.sub(r'[^\s\u0600-\u06FF]', '', str(text))

    #Remove Diacriticts
    text = remove_diacritics(text)

    text = remove_arabic_digits(text)

    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)

    # Remove leading ال from words
    text = re.sub(r'\bال', '', text)
    text = re.sub(r'\bوال', '', text)
    text = re.sub(r'(.)\1+', r'\1\1', text)

    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = text.replace('اا', 'ا')

    text = re.sub(r'\b\w{1}\b', '', text)

    # Remove multiple whitespace characters
    text = re.sub('\s+', ' ', text)

    return text.strip()

def remove_empty_cells(dataset):
    return dataset[dataset['cleaned_reviews'].str.len() > 0]

def drop_duplicate(dataset, column_name):
    return dataset.drop_duplicates(subset=[column_name])

