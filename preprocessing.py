import string
import nltk
from nltk.corpus import stopwords

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
    #TODO : todo
    return word

def removeStopWords(tokens):
    filtered_words = [word for word in tokens if word not in stopwords.words('english')]
    return filtered_words
