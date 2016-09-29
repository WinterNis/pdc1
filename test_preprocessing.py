import pytest
import preprocessing

#########################
# Unit tests for preprocessing functions
#########################

def test_tokenization():
    toTokenize = "\"Text to tokenize, i.e. untokenized text, has to be tokenized. It has to be tokenized as soon as possible\""
    tokens = ["text", "to", "tokenize", "i.e.", "untokenized", "text", "has", "to", "be", "tokenized", "it", "has", "to", "be", "tokenized", "as", "soon", "as", "possible"]
    tokensToTest = preprocessing.tokenize(toTokenize)
    for a, b in zip(tokens, tokensToTest):
        assert(a == b)

def test_stemming():
    assert(preprocessing.stem("tokenized") == "token")
    assert(preprocessing.stem("stemmer") == "stem")
    assert(preprocessing.stem("algorithmic") == "algorithm")
