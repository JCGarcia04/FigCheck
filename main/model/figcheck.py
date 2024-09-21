# FIGCHECK: Implementation of Natural Language Processing on Filipino Grammar Checking for Basic Education Students
# Full Python Code

# Garcia, John Clarenz C.
# Ramos, David Andre T.
# Sablan, Joshua Andrei D.
# Santos, Jun Nathan G.

import csv                       # For reading dictionary from csv file
import nltk                      # For splitting text into sentences
import re                        # For splitting sentence into words
from fuzzywuzzy import fuzz      # For spell checking

# For prediction
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

nltk.download('punkt_tab')

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
    suggsested = []
    acceptance_score = 85

    for correct_word in filipino_dictionary:
        score = fuzz.ratio(word, correct_word)
        if score >= acceptance_score:
            suggsested.append(correct_word)

    return suggsested

# Function for predicting
def predict(sentences):
    model = load_model('main/model/figcheck_model.keras')

    X_pred = np.array(sentences)
    print(X_pred)
    tokenizer = Tokenizer()

    tokenizer.fit_on_texts(X_pred)
    print(X_pred)
    X_pred = tokenizer.texts_to_sequences(X_pred)
    print(X_pred)
    max_length = model.input_shape[1]
    X_pred = pad_sequences(X_pred, padding='pre', maxlen=max_length)
    print(X_pred)
    y_pred = model.predict(X_pred)
    print(y_pred)
    y_pred = (y_pred > 0.5).astype(int)
'''
    if y_pred == 1:
        print('Grammatical error detected.')
    elif y_pred == 0:
        print('Sentence is gramatically correct.')
'''

def figcheck(text):
    sentences = split_into_sentences(text)

    split_sentences = []
    for i in range(len(sentences)):
        word_list = split_into_words(sentences[i])
        word_list.remove('')
        split_sentences.append(word_list)

    modified_sentences = []
    for j in range(len(sentences)):
        generalized = generalize(split_sentences[j])
        modified_sentences.append(generalized)

    dictionary, filipino_dictionary = read_files()

    all_mispelled = []
    suggestions = {}

    for s in modified_sentences:
        mispelled = check_words(s, dictionary)
        if len(mispelled) > 0:
            for m in mispelled:
                all_mispelled.append(m)

    if len(all_mispelled) != 0:
        for m in all_mispelled:
            suggested = correct_spelling(m, filipino_dictionary)
            suggestions[m] = suggested

    # Highlight the incorrect words in the original text
    highlighted_text = text
    for word in suggestions.keys():
        highlighted_text = highlighted_text.replace(word, f'<span class="error" data-suggestions="{", ".join(suggestions[word])}">{word}</span>')

    # Return a JSON response
    return {
        "highlighted_text": highlighted_text,
        "errors": [{"word": k, "suggestions": v} for k, v in suggestions.items()]
    }


# Main
# user_input = '1'
# while (user_input != '0'):
#     text = input("Enter a Filipino text: ")
#     sentences = split_into_sentences(text)

#     split_sentences = []
#     for i in range(len(sentences)):
#         word_list = split_into_words(sentences[i])
#         word_list.remove('')
#         split_sentences.append(word_list)

#     modified_sentences = []
#     for j in range(len(sentences)):
#         generalized = generalize(split_sentences[j])
#         modified_sentences.append(generalized)

#     dictionary, filipino_dictionary = read_files()

#     all_mispelled = []
#     for s in modified_sentences:
#         mispelled = check_words(s, dictionary)
#         if len(mispelled) > 0:
#             for m in mispelled:
#                 all_mispelled.append(m)

#     suggestions = {}

#     if len(all_mispelled) != 0:
#         for m in all_mispelled:
#             suggested = correct_spelling(m, filipino_dictionary)
#             suggestions[m] = suggested
#         print(suggestions)
#     else:

#         joined = []
#         for s in modified_sentences:
#             joined.append(' '.join(s))
#         predict(joined)
