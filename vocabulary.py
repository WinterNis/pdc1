import os
import glob
import gc
import mmap

import psutil
from sortedcontainers import SortedDict

from preprocessing import tokenize


class Vocabulary:

    def __init__(self, doc_dir, score_function, pl_dir='./pl', temp_dir='./pl', max_memory_use=0.5):

        self.doc_dir = doc_dir
        self.pl_files_directory = pl_dir  # default directory for the temp files storage
        self.temp_dir = temp_dir
        self.pl_files_count = 0  # count for temp file identification
        self.merged_file = None
        self.mem_map_file = None
        self.docs_token_counts = {}  # contains the number of tokens per doc
        self.voc_dict = {}  # contains the final vocabulary structure
        self.max_memory_use = max_memory_use

        if not os.path.exists(self.pl_files_directory):  # create the pl containing folder
            os.makedirs(self.pl_files_directory)
        if not os.path.exists(self.temp_dir):  # create the temp pl containing folder
            os.makedirs(self.temp_dir)

        if self.doc_dir:
            self.generate_voc()

    def generate_voc(self):
        """Generate the vocabulary index from the files in doc_dir, and store it in voc dict"""
        py_process = psutil.Process(os.getpid())

        # the schema of the posting_file is : word:[postingList]
        posting_file = SortedDict()  # temporary structure

        for filepath in glob.glob(os.path.join(self.doc_dir, 'la*')):

            doc_id = os.path.basename(filepath)[2:]

            with open(filepath, 'r') as f:
                file_content = f.read()

                # tokenization
                tokens = tokenize(file_content)

                # stemming

                # stop words removal

                self.docs_token_counts[doc_id] = len(tokens)

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
            if memory_use > self.max_memory_use:  # if memory usage exceed 500 mo
                self.flush_pl_to_disk(posting_file)
                posting_file = SortedDict()
                gc.collect()  # Force the garbage collection of the object

        self.flush_pl_to_disk(posting_file)  # flush the remaining pl to the disk
        self.merge_pl()

        self.merged_file = open(os.path.join('pl', 'PL_MERGED'), 'r+')
        self.mem_map_file = mmap.mmap(self.merged_file.fileno(), 0)

    def close(self):
        """Correctly close the pl file"""
        self.merged_file.close()
        self.mem_map_file.close()

    def flush_pl_to_disk(self, posting_file):
        """Write the posting_list as a temporary file"""
        filename = os.path.join(self.temp_dir, 'pl_temp_' + str(self.pl_files_count))
        with open(filename, 'w+') as f:
            for word, pl in posting_file.items():
                f.write(word)
                for doc_id, score in pl.items():
                    f.write(' ' + doc_id + ' ' + str(score))
                f.write('\n')
        self.pl_files_count += 1

    def merge_pl(self):
        """Merge the temporary pl files to one file"""
        filename = os.path.join(self.pl_files_directory, 'PL_MERGED')
        merged_file = open(filename, 'w+')

        file_list = []  # contains the file desriptors and the current line splitted
        words = []  # contains the current word for each file

        # initialize the file descriptors containers and word array
        for filepath in glob.glob(os.path.join(self.temp_dir, 'pl_temp_*')):
            f = open(filepath, 'r')
            l = f.readline().split()
            file_list.append([f, l[1:]])
            words.append(l[0])

        min_word = None
        while file_list:
            min_word = min(words)  # we search the minimal word (lexicographic order)
            doc_id_lists = []  # contains lists of doc_ids+score to be merged
            f_index = 0
            while f_index < len(file_list):
                file = file_list[f_index]
                if words[f_index] == min_word:
                    t = file[1]
                    doc_id_lists.append(list(zip(t[::2], t[1::2])))  # OP function to obtain pairs from the list
                    l = file[0].readline()  # read a new line
                    if l == '':
                        # the file is empty, it can be removed from the list
                        file_list[f_index][0].close()
                        del file_list[f_index]
                        del words[f_index]
                    else:
                        t = l.split()
                        file[1] = t[1:]  # ignore the first word
                        words[f_index] = t[0]  # update the file current word
                        f_index += 1
                else:
                    f_index += 1
            # merge the doc_id list
            pl = []  # will contain the current word posting_list
            while doc_id_lists:
                min_doc_id = min([a[0][0] for a in doc_id_lists])  # find the min doc_id in the lists
                pl.append([min_doc_id, 0])
                d_index = 0
                while d_index < len(doc_id_lists):
                    if doc_id_lists[d_index][0][0] == min_doc_id:  # we look for the first doc_id
                        pl[-1][1] += int(doc_id_lists[d_index][0][1])  # update the score
                        del doc_id_lists[d_index][0]
                        if not doc_id_lists[d_index]:  # the pl list is empty and can  be removed
                            del doc_id_lists[d_index]
                        else:
                            d_index += 1
                    else:
                        d_index += 1

            self.voc_dict[min_word] = [len(pl), merged_file.tell()]
            # Write the pl to the merged file
            for l in pl:
                merged_file.write(str(l[0]) + ' ' + str(l[1]) + ' ')
            merged_file.write('\n')

        merged_file.close()

    def access_pl(self, word):
        """Return the posting list of a word"""
        offset = self.voc_dict[word][1]
        print(self.voc_dict[word])
        self.mem_map.seek(offset)
        pl = self.mem_map.readline().split()
        return list(zip(pl[::2], pl[1::2]))
