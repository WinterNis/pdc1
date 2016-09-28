import glob
import string
import nltk


def tokenize(text):
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    tokens = nltk.word_tokenize(text)
    return tokens

# //////////////////////////////////////////////////////////////////////////////

voc_dict = {}

for filename in glob.glob('./latimes/la*'):
    with open(filename, 'r') as f:
        for line in f:

            # tokenization
            tokens = tokenize(line)

            # stemming

            # stop words removal
