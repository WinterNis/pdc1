import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *

#########################
# Preprocessing functions
#########################

# Breaks the given text up into a list of words (tokens)
def tokenize(text):
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    tokens = nltk.word_tokenize(text)
    return tokens

# Returns a stemmed version of the given word_tokenize
def stem(word):
    stemmer = PorterStemmer()
    return stemmer.stem(word)

# Removes stop words from a list of tokens
def removeStopWords(tokens):
    filtered_words = [word for word in tokens if word not in stopwords.words('english')]
    return filtered_words
