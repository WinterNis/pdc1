from vocabulary import Vocabulary
from scoring import calculateDocumentScore


def run():
    voc = Vocabulary('latimes', calculateDocumentScore)
    voc.close()

run()
