from vocabulary import Vocabulary
from scoring import calculateDocumentScore
from query import basic_and_query


def run():
    voc = Vocabulary('latimes', calculateDocumentScore)

    basic_and_query(voc, ['definitely'])  # test

    voc.close()

run()
