# FIGCHECK: Implementation of Natural Language Processing on Filipino Grammar Checking for Basic Education Students
# Full Python Code for Grammar and Spelling Checker

# Garcia, John Clarenz C.
# Ramos, David Andre T.
# Sablan, Joshua Andrei D.
# Santos, Jun Nathan G.

import csv                       # For reading dictionary from csv file
import nltk                      # For splitting text into sentences
import re                        # For splitting sentence into words
import pickle                    # For tokenizer
from fuzzywuzzy import fuzz      # For spell checking

# For prediction
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

# Function for setup
def set_up():
    nltk.download('punkt')
    nltk.download('punkt_tab')
    with open('main/model/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer, load_model('main/model/figcheck_model.h5')

# Function for splitting a text into sentences
def split_into_sentences(text):
    tokens = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)
    return sentences

# Function for splitting a sentence into words
def split_into_words(sentence):
    pattern = r"[\s\-,\.;:\u2013\u2014()\s]+"
    return re.split(pattern, sentence)

# Function for generalizing special words
def generalize(word_list):
    modified = []
    for _ in range(len(word_list)):
        # Character
        if (len(word_list[_]) == 1) and word_list[_].isupper():
            modified.append("CHAR")
        # Acronym
        elif (word_list[_][:-1].isupper()):
            modified.append("ACR")
        # Name
        elif (word_list[_][0].isupper() == True) and (_ != 0):
            modified.append("NAME")
        # Number
        elif (word_list[_].isdigit() == True):
            modified.append("NUM")
        # Percent
        elif word_list[_][-1] == '%':
            modified.append("PRCNT")
        else:
            hasNumber = False
            for c in word_list[_]:
                # Contains Number
                if c.isdigit() == True:
                    hasNumber = True
                    modified.append("HASNUM")
                    break
            if hasNumber == False:
                modified.append(word_list[_])
    return modified

# Function for reading csv files
def read_files():
    dictionary = []
    with open('main/model/figcheck_word_dictionary.csv', mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row:
              dictionary.append(row[0])

    filipino_dictionary = []
    with open('main/model/figcheck_word_dictionary.csv', mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row:
              filipino_dictionary.append(row[0])

    return dictionary, filipino_dictionary

# Function for checking if word exists in the dictionary
def check_words(sentence, dictionary):
    mispelled = []
    for w in sentence:
        word = w.lower()
        if word in ['char', 'acr', 'name', 'num', 'prcnt', 'hasnum']:
            continue
        elif word not in dictionary:
            mispelled.append(word)
    return mispelled

# Function for correction of spelling
def correct_spelling(word, filipino_dictionary):
    suggested = []
    acceptance_score = 85

    for correct_word in filipino_dictionary:
        score = fuzz.ratio(word, correct_word)
        if score >= acceptance_score:
            suggested.append(correct_word)

    return suggested

# Function for predicting
def predict(tokenizer, model, sentences):
    X_pred = np.array(sentences)
    X_pred = tokenizer.texts_to_sequences(X_pred)
    max_length = model.input_shape[1]
    X_pred = pad_sequences(X_pred, padding='pre', maxlen=max_length)

    y_pred = model.predict(X_pred)
    y_pred = (y_pred > 0.5).astype(int)
    
    return y_pred

def figcheck(text, tokenizer, model):
    # Split the text into sentences for grammar prediction
    sentences = split_into_sentences(text)
    
    # Split sentences into words for spell checking
    split_sentences = [split_into_words(sentence) for sentence in sentences]
    
    # Remove empty lists
    split_sentences = [words for words in split_sentences if words]

    # Generalize words for spell checking
    modified_sentences = [generalize(words) for words in split_sentences]

    # Load dictionaries
    dictionary, filipino_dictionary = read_files()

    # Check for misspelled words
    all_mispelled = []
    for words in modified_sentences:
        mispelled = check_words(words, dictionary)
        all_mispelled.extend(mispelled)

    # Generate suggestions for misspelled words
    suggestions = {}
    if all_mispelled:
        for word in set(all_mispelled):
            suggested = correct_spelling(word, filipino_dictionary)
            suggestions[word] = suggested

    # Prepare for grammar predictions
    joined_sentences = [' '.join(words) for words in modified_sentences]
    grammar_predictions = predict(tokenizer, model, joined_sentences)

    # Debug: Check what the predictions look like
    print("Grammar Predictions:", grammar_predictions)

    # Highlight incorrect words in the original text
    highlighted_text = text
    for word, suggestion in suggestions.items():
        highlighted_text = highlighted_text.replace(word, f'<span class="error" data-suggestions="{", ".join(suggestion)}">{word}</span>')

    # Return the structured results
    return {
        "highlighted_text": highlighted_text,
        "suggestions": suggestions,
        "grammar_predictions": grammar_predictions.tolist()  # Return dynamic predictions
    }
