import os
import glob

from sortedcontainers import SortedDict

pl_files_directory = './pl'  # default directory for the temp files storage
pl_files_count = 0  # count for temp file identification

if not os.path.exists(pl_files_directory):
    os.makedirs(pl_files_directory)


def flush_pl_to_disk(posting_file, path=pl_files_directory):
    global pl_files_count
    filename = os.path.join(path, 'pl_temp_' + str(pl_files_count))
    with open(filename, 'w+') as f:
        for word, pl in posting_file.items():
            f.write(word)
            for doc_id, score in pl.items():
                f.write(' ' + doc_id + ' ' + str(score))
            f.write('\n')
    pl_files_count += 1
    posting_file = SortedDict()


def merge_pl(voc_dict, temp_path=pl_files_directory, output_path=pl_files_directory):
    filename = os.path.join(output_path, 'PL_MERGED')
    merged_file = open(filename, 'w+')

    file_list = []  # contains the file desriptors and the current line splitted
    words = []  # contains the current word for each file

    # initialize the file descriptors containers and word array
    for filepath in glob.glob(os.path.join(temp_path, 'pl_temp_*')):
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

        voc_dict[min_word] = [len(pl), merged_file.tell()]
        # Write the pl to the merged file
        for l in pl:
            merged_file.write(str(l[0]) + ' ' + str(l[1]) + ' ')
        merged_file.write('\n')


    merged_file.close()
