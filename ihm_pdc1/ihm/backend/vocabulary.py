import os
import glob
import gc
import mmap
from collections import deque

import psutil
from sortedcontainers import SortedDict
import xml.etree.ElementTree as ET

from .preprocessing import tokenize
from .compression import pl_compress, pl_uncompress
from .document import DocumentRegistry


class Vocabulary:

    def __init__(self, doc_dir, score_function, pl_dir='pl', temp_dir='pl', max_memory_use=1, purge_temp=True):
        """Initialize the vocabulary object. If the doc_dir is None, saved voc structure will be
        load from disc"""

        self.absolute_path = os.path.dirname(os.path.realpath(__file__))
        self.doc_dir = doc_dir  # Directory containing the la* files
        self.pl_dir = pl_dir
        self.temp_dir = temp_dir  # default directory for the temp files storage
        self.pl_files_count = 0  # count for temp file identification
        self.merged_file = None
        self.mem_map_file = None
        self.score_function = score_function
        self.voc_dict = {}  # contains the final vocabulary structure
        self.max_memory_use = max_memory_use
        self.purge_temp = purge_temp
        self.document_registry = DocumentRegistry(self.pl_dir)

        if not os.path.exists(os.path.join(self.absolute_path, self.pl_dir)):  # create the pl containing folder
            os.makedirs(os.path.join(self.absolute_path, self.pl_dir))
        if not os.path.exists(os.path.join(self.absolute_path, self.temp_dir)):  # create the temp pl containing folder
            os.makedirs(os.path.join(self.absolute_path, self.temp_dir))

        if self.doc_dir:
            self.generate_voc()
        else:
            self.load_voc_from_disk()

        self.load_mm_file()

    def load_mm_file(self):
        filepath = os.path.join(self.absolute_path, 'pl', 'PL_MERGED')
        if not os.path.isfile(filepath):
            print('Pl file not existing, use index option')
            return
        self.merged_file = open(filepath, 'rb+')
        self.mem_map_file = mmap.mmap(self.merged_file.fileno(), 0)

    def generate_voc(self):
        """Generate the vocabulary index from the files in doc_dir, and store it in voc dict"""
        py_process = psutil.Process(os.getpid())

        # the schema of the posting_file is : word:[postingList]
        posting_file = SortedDict()  # temporary structure

        for filepath in glob.glob(os.path.join(self.absolute_path, self.doc_dir, 'la*')):

            with open(filepath, 'r') as f:
                root = ET.fromstring("<root>" + f.read() + "</root>")

            for doc in root:
                doc_id = doc.find('DOCID').text.strip()

                # tokenization
                doc_text = "".join(doc.itertext())
                tokens = tokenize(doc_text)

                # stemming

                # stop words removal

                self.document_registry.add_doc(doc_id, doc_text, len(tokens))

                for word in tokens:

                    # if the word is not in the index already
                    if word not in posting_file:

                        posting_file[word] = SortedDict(lambda x: int(x), {doc_id: 1})

                    # the word already exists (there is a line in posting_file)
                    else:
                        word_pl = posting_file[word]
                        if doc_id in word_pl:
                            word_pl[doc_id] += 1
                        else:
                            word_pl[doc_id] = 1

            memory_use = py_process.memory_info()[0]/2.**30  # memory use in GB
            if memory_use > self.max_memory_use:  # if memory usage exceed the limit
                self.flush_pl_to_disk(posting_file)
                posting_file = SortedDict()
                gc.collect()  # Force the garbage collection of the object

        self.flush_pl_to_disk(posting_file)  # flush the remaining pl to the disk
        self.merge_pl()

    def close(self):
        """Correctly close the pl file"""
        self.merged_file.close()
        self.mem_map_file.close()

    def flush_pl_to_disk(self, posting_file):
        """Write the posting_list as a temporary file"""
        if len(posting_file) != 0:
            filename = os.path.join(self.absolute_path, self.temp_dir, 'pl_temp_' + str(self.pl_files_count))

            with open(filename, 'w+') as f:
                for word, pl in posting_file.items():
                    f.write(word)
                    for doc_id, score in pl.items():
                        f.write(' ' + doc_id + ' ' + str(score))
                    f.write('\n')
            self.pl_files_count += 1

    def merge_pl(self):
        """Merge the temporary pl files to one file"""
        filename = os.path.join(self.absolute_path, self.pl_dir, 'PL_MERGED')
        merged_file = open(filename, 'wb+')

        file_list = []  # contains the file desriptors and the current line splitted
        words = []  # contains the current word for each file

        # initialize the file descriptors containers and word array
        for filepath in glob.glob(os.path.join(self.absolute_path, self.temp_dir, 'pl_temp_*')):
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
                    doc_id_lists.append(deque(zip(t[::2], t[1::2])))  # OP function to obtain pairs from the list
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
                min_doc_id = min([int(a[0][0]) for a in doc_id_lists])  # find the min doc_id in the lists
                pl.append([str(min_doc_id), 0])
                d_index = 0
                while d_index < len(doc_id_lists):
                    if int(doc_id_lists[d_index][0][0]) == min_doc_id:  # we look for the first doc_id
                        pl[-1][1] += int(doc_id_lists[d_index][0][1])  # update the score
                        doc_id_lists[d_index].popleft()  # efficient since it's a deque
                        if not doc_id_lists[d_index]:  # the pl list is empty and can be removed
                            del doc_id_lists[d_index]
                        else:
                            d_index += 1
                    else:
                        d_index += 1

            write_offset = merged_file.tell()
            # Write the pl to the merged file
            for l in pl_compress(pl):
                merged_file.write(l[0] + b'\u0130' + l[1] + b'\u0130')
            write_size = merged_file.tell() - write_offset
            self.voc_dict[min_word] = [write_offset, write_size]  # store the offset in the file

        merged_file.close()

        self.write_voc_to_disk()

        if self.purge_temp:
            for filepath in glob.glob(os.path.join(self.absolute_path, self.temp_dir, 'pl_temp_*')):
                os.remove(filepath)

    def access_pl(self, word_request):
        """Return the posting list of a word"""
        word = self.voc_dict.get(word_request)
        if word is None:
            return None
        offset, size = word[0], word[1]
        self.mem_map_file.seek(offset)
        line = self.mem_map_file.read(size).split(b'\u0130')

        u_pl = pl_uncompress(list(zip(line[::2], line[1::2])))

        pl = list(map(
            lambda x: (
                x[0],
                self.score_function(
                    int(x[1]),
                    self.document_registry.access_token_count(x[0]),
                    len(u_pl)/2,
                    self.document_registry.doc_count())),
            u_pl
            ))

        id_sorted_pl = SortedDict(pl)

        inverted_pl = [(str(p[1]), p[0]) for p in pl]
        score_sorted_pl = sorted(inverted_pl, key=lambda k: int(k[0]), reverse=True)

        return [id_sorted_pl, score_sorted_pl]

    def write_voc_to_disk(self):
        """Store the voc structure into a file, so it can be retrieved later"""

        filename = os.path.join(self.absolute_path, self.pl_dir, 'voc_index')

        with open(filename, 'w+') as f:
            for key, value in self.voc_dict.items():
                f.write(key + ' ' + str(value[0]) + ' ' + str(value[1]) + '\n')

    def load_voc_from_disk(self):
        """Load a saved voc struture from disc"""
        filename = os.path.join(self.absolute_path, self.pl_dir, 'voc_index')

        if not os.path.isfile(filename):
            print('Voc file not existing, use index option')
            return
        with open(filename, 'r') as f:
            for line in f:
                l = line.split()
                self.voc_dict[l[0]] = [int(l[1]), int(l[2])]

    def get_terms_dicts_for_docs(self):
        ret = {}
        for word in self.voc_dict.keys():
            pl = self.access_pl(word)[0]
            for doc_id, score in pl.items():
                if doc_id not in ret:
                    ret[doc_id] = {}
                ret[doc_id][word] = score
        return ret
