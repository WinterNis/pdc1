import os
import glob
import gc

import psutil
from sortedcontainers import SortedDict

from preprocessing import tokenize
from merged_based import flush_pl_to_disk, merge_pl


def run():
    py_process = psutil.Process(os.getpid())

    voc_dict = {}  # contains the final vocabulary structure

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

        memory_use = py_process.memory_info()[0]/2.**30  # memory use in GB
        print(memory_use)
        if memory_use > 0.5:
            flush_pl_to_disk(posting_file)
            posting_file = SortedDict()
            gc.collect()  # Force the garbage collection of the object

    merge_pl(voc_dict)


run()
