mport pytest
import preprocessing

#########################
# Unit tests for preprocessing functions
#########################

def test_tokenization():
    toTokenize = "\"Text to tokenize (in fact, untokenized text), has to be tokenized. It has to be tokenized as soon as possible\""
    tokens = ["text", "to", "tokenize", "in", "fact", "untokenized", "text", "has", "to", "be", "tokenized", "it", "has", "to", "be", "tokenized", "as", "soon", "as", "possible"]
    tokensToTest = preprocessing.tokenize(toTokenize)
    for a, b in zip(tokens, tokensToTest):
        assert(a == b)

def test_stemming():
    wordsToStem = ["tokenized", "roses", "brutally", "dozens", "stupidity", "notorious", "english", "stemming", "stemmed", "soft"]
    for i in range(0, len(wordsToStem)-1):
        wordsToStem[i] = preprocessing.stem(wordsToStem[i])
    stemmedWords = ["token", "rose", "brutal", "dozen", "stupid", "notori", "english", "stem", "stem", "soft"]
    for a, b in zip(wordsToStem, stemmedWords):
        assert(a == b)

def test_removeStopWords():
    tokensToFilter = ["In", "this", "text", "stop", "words", "have", "to", "be", "removed", "In", "each", "phrase", "occurances", "of", "words", "such", "as", "this", "that", "so", "and", "and", "of", "will", "be", "removed"]
    filteredTokens = ["In", "text", "stop", "words", "removed", "In", "phrase", "occurances", "words", "removed"]
    tokensToTest = preprocessing.removeStopWords(tokensToFilter)
    for a, b in zip(filteredTokens, tokensToTest):
        assert(a == b)
