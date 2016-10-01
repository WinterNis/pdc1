import os
import glob

from preprocessing import tokenize
from sortedcontainers import SortedDict


def run():
    voc_dict = {}

    # the schema of the posting_file is : word:[postingList]
    posting_file = SortedDict()

    for filepath in glob.glob('./latimes/la*'):
        doc_id = os.path.basename(filepath)[2:]

        with open(filepath, 'r') as f:
            file_content = f.read()

            # tokenization
            tokens = tokenize(file_content)

            # stemming

            # stop words removal

            for word in tokens:

                # if the word is not in the index already
                if word not in posting_file:

                    posting_file[word] = SortedDict({doc_id: 1})


                # the word already exists (there is a line in posting_file)
                else:
                    word_pl = posting_file[word]
                    if doc_id in posting_file[word]:
                        word_pl[doc_id] += 1
                    else:
                        word_pl[doc_id] = 0

    voc_dict = posting_file


run()