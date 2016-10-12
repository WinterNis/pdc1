from operator import itemgetter

#TODO write unit test and test
def basic_or_query(voc, searchTermsList):
    """Find the docID documents where any of the listed terms ('OR' type query) in searchTermsList
    appear and sort them by their score we work on a finished inverted file from
    which we use interface functions"""

    results = {} # { "docID" => score }
    PLList = list()

    for searchTerm in searchTermsList:
        PLList.append(voc.access_pl(searchTerm)[0])

    PLList = sorted(PLList, key=len)

    # for each docID-score in each PL, add score in results dictionary
    for pl in PLList:
        for docID, score in pl.items():
            if docID in results:
                results[docID] += score
            else:
                results[docID] = score

    #resultsList = sorted(results.keys(), reverse=1) # sort by score
    resultsList = list()
    for key in results.keys():
        resultsList.append([key, results[key]])

    resultsList = sorted(resultsList, key=itemgetter(1), reverse=1)  # sort by score
    
    return resultsList

def basic_and_query(voc, searchTermsList):
    """Find the docID where all the terms ('AND' type query) in searchTermsList
    appear and sort them by their score we work on a finished inverted file from
    which we use interface functions"""

    resultsList = list()  # contains the docIds sorted by their score

    # first we get the PL for the terms and store them in a list
    PLList = list()  # PLList is going to contain all PL for each searchTerm

    for searchTerm in searchTermsList:
        # getPLForTerm() is an interface function that return the posting list of a term
        searchTermPL = voc.access_pl(searchTerm)[0]

        PLList.append(searchTermPL)  # we store the PL associated to the searchTerm

    PLList = sorted(PLList, key=len)  # we sorted the list by the PL length

    # we go over each PL sorted by DocID but from the smallest to the biggest
    # we add to results all of the first PL,
    # then we remove all that do not appear in the second PL, then in the third PL, etc..
    # we update the score on live
    smallestPL = PLList.pop(0)

    for docID, score in smallestPL.items():
        for PL in PLList:

            scoreInPL = PL.get(docID)

            if scoreInPL is None:
                score = -1
                break
            else:
                score += scoreInPL

        if score > 0:
            resultsList.append([docID, score])

    resultsList = sorted(resultsList, key=itemgetter(1), reverse=1)  # sort by score

    return resultsList
