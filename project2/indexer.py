from collections import Counter
from collections import OrderedDict

from linkedlist import LinkedList


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        self.doc_count = 0

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        self.doc_count += 1
        counts = Counter(tokenized_document)
        for term, term_count in counts.items():
            self.add_to_index(term, doc_id, len(tokenized_document), term_count)

    def add_to_index(self, term_, doc_id_, docs, term_count):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the postings list of the term.
            To be implemented."""
        if term_ not in self.inverted_index or self.inverted_index[term_] is None:
            postings_linked_list = LinkedList()
            postings_linked_list.insert_at_end_with_tf(doc_id_, docs, term_count)
            self.inverted_index[term_] = postings_linked_list
        else:
            self.inverted_index[term_].insert_at_end_with_tf(doc_id_, docs, term_count)

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        for term, postings_list in self.get_index().items():
            postings_list.add_skip_connections()

    def calculate_tf_idf(self):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
        for term, postings_list in self.get_index().items():
            idf = float(self.doc_count / postings_list.length)
            postings_list.set_idf_score(idf)
            if postings_list.start_node is None:
                return
            else:
                n = postings_list.start_node
                while n is not None:
                    tf = float(n.frequency / n.tdf)
                    n.set_tf(tf)
                    tf_idf = tf * idf
                    n.set_tf_idf(tf_idf)
                    n = n.next

    def get_postings_list(self, term):
        if term in self.get_index():
            return self.get_index()[term].traverse_list()
        else:
            return []

    def get_skip_postings_list(self, term):
        if term in self.get_index():
            return self.get_index()[term].traverse_skips()
        else:
            return []