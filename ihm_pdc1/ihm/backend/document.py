import os.path

from sortedcontainers import SortedDict


class DocumentRegistry:

    def __init__(self, doc_dir):
        self.absolute_path = os.path.dirname(os.path.realpath(__file__))
        self.document_registry = SortedDict(lambda x: int(x), {})
        self.doc_file_path = os.path.join(self.absolute_path, doc_dir, 'documents')
        self.doc_index_file_path = os.path.join(self.absolute_path, doc_dir, 'document_index')
        self.load_doc_registry()

    def add_doc(self, doc_id, text, tokenCount):
        if doc_id not in self.document_registry:
            with open(self.doc_file_path, 'a') as doc_file:
                start = doc_file.tell()
                doc_file.write(text)
                size = doc_file.tell() - start
                doc_file.close()
                self.document_registry[doc_id] = [start, size, tokenCount]
                with open(self.doc_index_file_path, 'a') as doc_index:
                    doc_index.write(str(doc_id) + ' ' + str(start) + ' ' + str(size) + ' ' + str(tokenCount) + '\n')
        else:
            # Remove the document from the file and re-write-it
            # Remove also from index
            # TODO
            pass

    def access_doc(self, doc_id):
        with open(self.doc_file_path, 'r') as doc_file:
            doc = self.document_registry[doc_id]
            doc_file.seek(doc[0])
            text = doc_file.read(doc[1])
        return text

    def access_token_count(self, doc_id):
        return self.document_registry.get(doc_id, None)[2]

    def doc_count(self):
        return len(self.document_registry)

    def load_doc_registry(self):
        if os.path.isfile(self.doc_index_file_path):
            with open(self.doc_index_file_path, 'r') as doc_index:
                for l in doc_index:
                    line = l.split()
                    self.document_registry[line[0]] = list(map(int, line[1:]))
