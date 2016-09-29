# For one posting list (one term), calculate score based on the number of occurence of the term in each document and total number of terms per documents
def calculatePostingListScore(postingList, docsTokenCounts):
	newPostingList = []

	for post in postingList:
		# post has a list [documentName, occurenceCount]
		docName = post[0]

		# Find Total count based on document name
		tokenCount = docsTokenCounts[docName]

		# Calculate term-frequency
		tf = post[1] / tokenCount

		# Save it to new posting list
		newPostingList += [[docName, tf]]

	return newPostingList


def testCalculatePostingListScore():
	postingList = [["a.doc", 3], ["b.doc", 2], ["c.doc", 1], ["d.doc", 7]]

	docsTokenCounts = {"a.doc": 20, "b.doc": 20, "c.doc": 20, "d.doc": 20}

	print('Posting List before calulation : ' + repr(postingList))

	postingList = calculatePostingListScore(postingList, docsTokenCounts)

	print('Posting List before calulation : ' + repr(postingList))

testCalculatePostingListScore()
