import argparse
import timeit

from .vocabulary import Vocabulary
from .scoring import calculateDocumentScore
from .query import basic_and_query
from .query import basic_or_query
from .fagin import fagin
from .preprocessing import preprocessQuery, find_query_type
from .clustering import clustering_process_for_best_results_query

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', action='store_true')
    args = parser.parse_args()

    voc = None

    if args.index:
        start_time = timeit.default_timer()
        voc = Vocabulary('latimes', calculateDocumentScore)
        index_time = timeit.default_timer() - start_time
        print('Indexation took ' + str(index_time) + ' seconds')
    else:
        voc = Vocabulary(None, calculateDocumentScore)

    query = ''

    while(1):
        query = input("Query? ")

        if query == '/quit':
            break
        start_time = timeit.default_timer()
        result = basic_and_query(voc, query)
        exec_time = timeit.default_timer() - start_time
        for r in result:
            print(str(r[0]) + ' ' + str(r[1]))
        print('Query executed in ' + str(exec_time) + ' seconds')

    voc.close()


def generate_index():
    """For django call"""
    start_time = timeit.default_timer()
    voc = Vocabulary('latimes', calculateDocumentScore)
    index_time = timeit.default_timer() - start_time
    print('Indexation took ' + str(index_time) + ' seconds')


def search_words(query):
    """For django call"""
    try:
        voc = Vocabulary(None, calculateDocumentScore)
    except:
        return "Missing file"

    list_query = preprocessQuery(query)
    result = []

    # we check if we want a conjonctive or a disjunctive request
    is_conjonctive_query = find_query_type(query)
    if is_conjonctive_query:
        # we do a conjonctive request
        result = fagin(voc, list_query, 10, True)
        # result = basic_and_query(voc, list_query)
        print("conjonctive")
        print(list_query)
    else:
        # we do the disjunctive trick with Fagin or naive algo
        result = fagin(voc, list_query, 10, False)
        # result = basic_or_query(voc, list_query)
        print("disjonctive")
        print(list_query)

    doc_id_clusters_dict,describing_words_clusters_lists_dict = clustering_process_for_best_results_query(voc, result, number_of_keys_to_considered=3, number_of_clusters_wanted=3, number_of_describing_words=3)

    ret = []
    for r in result:
        cluster_number_for_r = doc_id_clusters_dict[r[0]]
        describing_words_list = describing_words_clusters_lists_dict[cluster_number_for_r]
        ret.append([r[0], r[1], voc.document_registry.access_doc(r[0]),"\nCLUSTERING : \n",cluster_number_for_r,describing_words_list])
        #ret.append([r[0], r[1], voc.document_registry.access_doc(r[0])])

    return ret
