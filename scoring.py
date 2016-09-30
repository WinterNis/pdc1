import math

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

		# Calculate idf
		idf = math.log(len(docsTokenCounts)/len(postingList))

		# calculate score
		score = tf * idf

		# Save it to new posting list
		newPostingList += [[docName, score]]

	return newPostingList
