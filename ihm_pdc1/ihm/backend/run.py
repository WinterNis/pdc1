import argparse
import timeit

from .vocabulary import Vocabulary
from .scoring import calculateDocumentScore
from .query import basic_and_query
from .fagin import fagin
from .preprocessing import preprocessQuery


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
    voc = Vocabulary('latimes', calculateDocumentScore)


def search_words(query):
    """For django call"""
    try:
        voc = Vocabulary(None, calculateDocumentScore)
    except:
        return "Missing file"

    result = fagin(voc, query, 10, True)
    return result
