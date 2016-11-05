import timeit

from .vocabulary import Vocabulary
from .scoring import calculateDocumentScore
from .fagin import fagin
from .preprocessing import preprocessQuery, find_query_type
from .clustering import clustering_process_for_best_results_query


def generate_index():
    """For django call"""
    start_time = timeit.default_timer()
    voc = Vocabulary('latimes', calculateDocumentScore)
    index_time = timeit.default_timer() - start_time
    print('Indexation took ' + str(index_time) + ' seconds')


def search_words(query):
    """For django call"""
    voc = Vocabulary(None, calculateDocumentScore)

    start_time = timeit.default_timer()
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

    index_time = timeit.default_timer() - start_time
    print('Query took ' + str(index_time) + ' seconds')

    start_time = timeit.default_timer()
    doc_id_clusters_dict, describing_words_clusters_lists_dict = clustering_process_for_best_results_query(voc, result, number_of_keys_to_considered=3, number_of_clusters_wanted=3, number_of_describing_words=3)
    index_time = timeit.default_timer() - start_time
    print('Clustering took ' + str(index_time) + ' seconds')

    ret = []
    for r in result:

        cluster_number_for_r = doc_id_clusters_dict[r[0]]
        describing_words_list = describing_words_clusters_lists_dict[cluster_number_for_r]

        start_time = timeit.default_timer()
        ret.append([r[0], r[1], voc.document_registry.access_doc(r[0]), "\nCLUSTERING : \n", cluster_number_for_r, describing_words_list])
        index_time = timeit.default_timer() - start_time
        print('Appending took ' + str(index_time) + ' seconds')
        #  ret.append([r[0], r[1], voc.document_registry.access_doc(r[0])])

    return ret
