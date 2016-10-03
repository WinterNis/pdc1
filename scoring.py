import math


def calculatePostingListScore(postingList, docsTokenCounts):
    """For one posting list (one term), calculate score based on the number of
    occurence of the term in each document and total number of terms per documents"""
    newPostingList = []

    for post in postingList:
        # post has a list [documentName, occurenceCount]
        docName = post[0]

        # Find Total count based on document name
        tokenCount = docsTokenCounts[docName]

        score = calculateDocumentScore(post[1], tokenCount, len(postingList), len(docsTokenCounts))

        # Save it to new posting list
        newPostingList += [[docName, score]]

    return newPostingList


def calculateDocumentScore(termDocumentCount, docTokenCounts, numberOfDocsContainingTerm, totalNumberOfDocs):
    # Calculate term-frequency
    tf = termDocumentCount / docTokenCounts

    # Calculate idf
    idf = math.log(totalNumberOfDocs/numberOfDocsContainingTerm)

    # Calculate score
    score = tf * idf

    return score
