import math


class Node:

    def __init__(self, value=None, next=None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.skip_node = None
        self.frequency = 0
        self.tdf = 0.0
        self.tf = 0.0
        self.tf_idf = 0.0

    def set_skip_pointer(self, node):
        self.skip_node = node

    def set_tf(self, score_tf):
        self.tf = score_tf

    def set_tf_idf(self, score_tf_idf):
        self.tf_idf = score_tf_idf


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""

    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None

    def set_idf_score(self, idf_score):
        self.idf = idf_score

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            print("List has no element")
            return
        else:
            n = self.start_node
            # Start traversal from head, and go on till you reach None
            while n is not None:
                traversal.append(n.value)
                n = n.next
            return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            skip_n = self.start_node
            while skip_n is not None:
                traversal.append(skip_n.value)
                skip_n = skip_n.skip_node
            return traversal

    def add_skip_connections(self):
        """ Write logic to add skip pointers to the linked list.
                    This function does not return anything.
                    To be implemented."""
        n_skips = math.floor(math.sqrt(self.length))
        if n_skips * n_skips == self.length:
            n_skips = n_skips - 1

        self.skip_length = n_skips
        skips = round(math.sqrt(self.length), 0)

        if skips > 1:
            count = 0
            skip_length = 1
            start = self.start_node
            while start:
                if count % skips == 0:
                    node = start
                    skip_count = 0
                    while node and skip_count < skips:
                        node = node.next
                        skip_count += 1

                    if node is not None:
                        start.set_skip_pointer(node)
                        skip_length += 1
                count += 1
                start = start.next

    def insert_at_end(self, value):
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
            To be implemented. """
        new_node = Node(value=value)
        self.insert_node_at_end(new_node)

    def insert_at_end_with_tf(self, value, docs, term_count):
        new_node = Node(value=value)
        new_node.tdf = docs
        new_node.frequency = term_count
        self.insert_node_at_end(new_node)

    def insert_at_end_with_tf_idf(self, value, tf_idf):
        new_node = Node(value=value)
        new_node.tf_idf = tf_idf
        self.insert_node_at_end(new_node)

    def insert_node_at_end(self, new_node):
        value = new_node.value
        n = self.start_node
        self.length += 1

        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
            return

        elif self.start_node.value >= value:
            if self.start_node.value == value:
                return
            self.start_node = new_node
            self.start_node.next = n
            return

        elif self.end_node.value <= value:
            if self.end_node.value == value:
                return
            self.end_node.next = new_node
            self.end_node = new_node
            return

        else:
            while n.value < value < self.end_node.value and n.next is not None:
                if n.value == value:
                    return
                n = n.next

            m = self.start_node
            while m.next != n and m.next is not None:
                m = m.next
            m.next = new_node
            new_node.next = n
            return


if __name__ == "__main__":
    l1 = LinkedList()
    for i in range(1, 17):
        if i % 2 == 0:
            l1.insert_at_end(i)

    print(l1.traverse_list())
    l1.add_skip_connections()
    print(l1.traverse_skips())

    l2 = LinkedList()
    l2.insert_at_end(1)
    l2.insert_at_end(2)
    l2.insert_at_end(5)
    l2.insert_at_end(6)
    l2.insert_at_end(7)
    l2.insert_at_end(10)
    l2.insert_at_end(16)
    l2.insert_at_end(17)

    print(l2.traverse_list())
    l2.add_skip_connections()
    print(l2.traverse_skips())
