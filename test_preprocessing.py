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

def test_removeStopWords():
    tokensToFilter = ["In", "this", "text", "stop", "words", "have", "to", "be", "removed", "In", "each", "phrase", "occurances", "of", "words", "such", "as", "this", "that", "so", "and", "and", "of", "will", "be", "removed"]
    filteredTokens = ["In", "text", "stop", "words", "removed", "In", "phrase", "occurances", "words", "removed"]
    tokensToTest = preprocessing.removeStopWords(tokensToFilter)
    for a, b in zip(filteredTokens, tokensToTest):
        assert(a == b)
