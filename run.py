import glob
import string
import nltk


def tokenize(text):
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    tokens = nltk.word_tokenize(text)
    return tokens

# //////////////////////////////////////////////////////////////////////////////

voc_dict = {}

#the schema of the posting_file is : (word,[postingList])
posting_file = []

for filename in glob.glob('./latimes/la*'):
    doc_id = filename[2:]

    with open(filename, 'r') as f:
        for line in f:

            # tokenization
            tokens = tokenize(line)

            # stemming

            # stop words removal

            for word in tokens:
                #if the word does not exists
                if word not in voc_dict:
                    #we must find the right place to put our new line corresponding to a word

                    index_insertion = 0

                    #TODO: we can make an dichotomy for more perfs
                    for i in range(len(posting_file)):
                        key_word = posting_file[0][0]
                        index_insertion = i
                        if word > key_word:
                            #we leave the loop
                            break

                    voc_dict[word] = [1, index_insertion]

                    #we add to the right position
                    posting_file.insert(index_insertion, (word,[filename, 1]))

                #the word already exists (there is a line in posting_file)
                else:

                    #we add to the right place
                    #TODO dichotomy !

                    index_insertion = 0
                    insert = False
                    for i in range(len(posting_file[word][1])):
                        index_insertion = i

                        #if the word is already present in this document, we increment
                        if filename == posting_file[word][1][i]:
                            posting_file[word][1][i][1] += 1
                            break
                        elif filename > posting_file[word][1][i]:
                            insert = True
                            break

                    if insert:
                        posting_file[word][1].insert(index_insertion, [filename, 1])


