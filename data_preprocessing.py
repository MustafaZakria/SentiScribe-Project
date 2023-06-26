import nltk
import re
import pyarabic.araby as araby
import emoji
from nltk.corpus import stopwords
import numpy as np
import streamlit as st

def remove_emoji(text):
    return emoji.demojize(text)

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

def negation(text):
    pattern = r"(ما|م)(\w*)ش"
    replacement = r"مش \2"
    return re.sub(pattern, replacement, text)

def negation_replacement(text):
  regex_pattern = r"\b(ليس|لم|لا|لن)\b"
  replacement = "مش"
  return re.sub(regex_pattern, replacement, text)

@st.cache_resource
def cleaning(text):
   Arabic_numbers = ['٤','١','٢','٣','٥','٦','٧','٨','٩','٠']
   special_character = ['؟','،','?',',','!','.',':','"','""','‘‘','‘','؛','↓',"'", '‰',
                      '`','€',';','ç','ı','À','@','٬','~᷂','٫','⁩◕','.',
                      '=','#','$','%','^','&','*','()',')','(','\\','/',
                      '((', '_', '"','"', '…','-','×','ツ','+','%','٪','⁩ლ']

   text= remove_emoji(text)
   #replace special characters with whitespaces
   for word in range(0, len(special_character)):
      text = text.replace(special_character[word], '')

   #replace  arabic numbers with whitespaces
   for word in range(0, len(Arabic_numbers)):
      text = text.replace(Arabic_numbers[word], '')

   # Using regex to remove all non-Arabic letters, digits, punctuation marks, and emojis
   text = re.sub(r'[^\u0600-\u06FF\u0660-\u0669\u06F0-\u06F9\s\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]+', '', text)
   #text = re.sub(r'(.)\1+', r'\1', text)

   p_longation = re.compile(r'(.)\1+')
   subst = r"\1\1"
   text = re.sub(p_longation, subst, text)
   text = text.replace('وو', 'و')
   text = text.replace('يي', 'ي')
   text = text.replace('اا', 'ا')

   text = negation(text)
   text = negation_replacement(text)

   #remove english words letters and numbers
   text = re.sub(r'[0-9a-zA-Z]+',' ', text)

   text = re.sub("[إأٱآا]", "ا", text)

   text = re.sub("ى", "ي", text)
   text = re.sub("ة", "ه", text)
   #text = remove_aatf(text)
   text = re.sub(r'\bال', '', text)
   text = re.sub('علي', '', text)
   text = remove_diacritics(text)

   return text


def stop_word_removal(text):
    stop_words = set(stopwords.words("arabic"))
    words = araby.tokenize(text)
    text = " ".join([w for w in words if not w in stop_words])
    return text

@st.cache_resource
def preprocessing(text):
  text = re.sub('\s+', ' ', str(text))
  text = araby.strip_tashkeel(text)
  text = cleaning(text)
  text = stop_word_removal(text)

  return text

def remove_empty_cells(dataset):
    dataset = dataset.replace("", np.nan)
    dataset = dataset.dropna()

    return dataset

def drop_duplicate(dataset, column_name):
    dataset = dataset.drop_duplicates(subset=[column_name])
    return dataset
