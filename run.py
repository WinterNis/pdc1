import os
import glob
import gc
import mmap

import psutil
from sortedcontainers import SortedDict

from preprocessing import tokenize
from merged_based import flush_pl_to_disk, merge_pl


def access_pl(voc_dict, mem_map, word):
    offset = voc_dict[word][1]
    print(voc_dict[word])
    mem_map.seek(offset)
    pl = mem_map.readline().split()
    return list(zip(pl[::2], pl[1::2]))


def run():
    py_process = psutil.Process(os.getpid())

    docs_token_counts = {}
    voc_dict = {}  # contains the final vocabulary structure

    # the schema of the posting_file is : word:[postingList]
    posting_file = SortedDict()  # temporary structure

    for filepath in glob.glob('./latimes/la*'):

        doc_id = os.path.basename(filepath)[2:]

        with open(filepath, 'r') as f:
            file_content = f.read()

            # tokenization
            tokens = tokenize(file_content)

            # stemming

            # stop words removal

            docs_token_counts[doc_id] = len(tokens)

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
                        word_pl[doc_id] = 1

        memory_use = py_process.memory_info()[0]/2.**30  # memory use in GB
        if memory_use > 0.5:  # if memory usage exceed 500 mo
            flush_pl_to_disk(posting_file)
            posting_file = SortedDict()
            gc.collect()  # Force the garbage collection of the object

    flush_pl_to_disk(posting_file)  # flush the remaining pl to the disk
    merge_pl(voc_dict)

    with open(os.path.join('pl', 'PL_MERGED'), 'r+') as f:
        mem_map_file = mmap.mmap(f.fileno(), 0)

        mem_map_file.close()


run()
