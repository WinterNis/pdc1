import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *

#########################
# Preprocessing functions
#########################

stop_word_set = set(stopwords.words('english'))

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
    filtered_words = [word for word in tokens if word not in stop_word_set]
    return filtered_words

# Applies preprocessing to query and returns list of tokens
def preprocessQuery(query):
    tokens = tokenize(query)
    removeStopWords(tokens)
    return tokens

# Return true if we find that query is conjonctive or false if it is disjonctive
# query is just text with words and keywords split by whitespaces
def find_query_type(query):
    keyword_disjonctive = "||"
    keyword_conjonctive = "&&"
    query_words_list = query.split()#contains words from query in a list
    if keyword_disjonctive in query_words_list:
        return False
    elif keyword_conjonctive in query_words_list:
        return True
    return True # default choice -> if we want conjonctive by default, return true, else return false
