def heapsort(l):
    """
    Sort a list using the heap (assuming there are no repeated values).
    
    >>> heapsort([1, 6, 2, 8, 9, 14, 4, 7])
    [1, 2, 4, 6, 7, 8, 9, 14]
    """
    q = PQueue()
    for (i, x) in enumerate(l): q.update(i, x)
    return [ q.pop_smallest()[1] for x in l ]

def _parent(i):
    """
    Returns the parent node of the given node.
    """
    return (i - 1) // 2
    
def _lchild(i):
    """
    Returns the left child node of the given node.
    """
    return 2 * i + 1
    
def _rchild(i):
    """
    Returns the right child node of the given node.
    """
    return 2 * i + 2
    
def _children(i):
    """
    Returns the children of the given node as a tuple (left then right).
    """
    return (_lchild(i), _rchild(i))

class PQueue:
    """
    Priority queue implemented with dictionaries. Stores a set of keys and associated priorities.
    
    >>> q = PQueue()
    >>> q.is_empty()
    True
    >>> q.update("thing", 5)
    True
    >>> q.is_empty()
    False
    >>> q.update("another thing", 2)
    True
    >>> q.pop_smallest()
    ('another thing', 2)
    >>> q.update("thing", 100)
    False
    >>> q.update("something else", 110)
    True
    >>> q.update("something else", 8)
    True
    >>> "thing" in q
    True
    >>> "nothing" in q
    False
    >>> len(q)
    2
    >>> q.peek_smallest()
    ('thing', 5)
    >>> q.pop_smallest()
    ('thing', 5)
    >>> q.pop_smallest()
    ('something else', 8)
    >>> True if q else False
    False
    >>> q.is_empty()
    True
    >>> q.tie_breaker = lambda x,y: x[1] < y[1]
    >>> q.update(("A", 6), 5)
    True
    >>> q.update(("B", 1), 5)
    True
    >>> q.update(("C", 10), 1)
    True
    >>> q.update(("D", 4), 5)
    True
    >>> q.pop_smallest()[0][0]
    'C'
    >>> q.pop_smallest()[0][0]
    'B'
    >>> q.pop_smallest()[0][0]
    'D'
    >>> q.pop_smallest()[0][0]
    'A'
    
    """
    def __init__(self):
        self._heap = []
        self._keyindex = {}
        self.tie_breaker = None
        
    def __len__(self):
        return len(self._heap)
        
    def __contains__(self, key):
        return key in self._keyindex 
        
    def _key(self, i):
        """
        Returns the key value of the given node.
        """
        return self._heap[i][0]
        
    def _priority(self, i):
        """
        Returns the priority of the given node.
        """
        return self._heap[i][1]
    
    def _swap(self, i, j):
        """
        Swap the positions of two nodes and update the key index.
        """
        (self._heap[i], self._heap[j]) = (self._heap[j], self._heap[i])
        (self._keyindex[self._key(i)], self._keyindex[self._key(j)]) = (self._keyindex[self._key(j)], self._keyindex[self._key(i)])
        
    def _heapify_down(self, i):
        """
        Solves heap violations starting at the given node, moving down the heap.
        """
        
        children = [ c for c in _children(i) if c < len(self._heap) ]
        
        # This is a leaf, so stop
        if not children: return
        
        # Get the minimum child
        min_child = min(children, key=self._priority)
        
        # If there are two children with the same priority, we need to break the tie
        if self.tie_breaker and len(children) == 2:
            c0 = children[0]
            c1 = children[1]
            if self._priority(c0) == self._priority(c1):
                min_child = c0 if self.tie_breaker(self._key(c0), self._key(c1)) else c1
        
        # Sort, if necessary
        a = self._priority(i)
        b = self._priority(min_child)
        if a > b or (self.tie_breaker and a == b and not self.tie_breaker(self._key(i), self._key(min_child))):
            # Swap with the minimum child and continue heapifying
            self._swap(i, min_child)
            self._heapify_down(min_child)
            
    def _heapify_up(self, i):
        """
        Solves heap violations starting at the given node, moving up the heap.
        """
        # This is the top of the heap, so stop.
        if i == 0: return
        
        parent = _parent(i)
        a = self._priority(i)
        b = self._priority(parent)
        if a < b or (self.tie_breaker and a == b and self.tie_breaker(self._key(i), self._key(parent))):
            self._swap(i, parent)
            self._heapify_up(parent)
            
    def peek_smallest(self):
        """
        Returns a tuple containing the key with the smallest priority and its associated priority.
        """
        return self._heap[0]
        
    def pop_smallest(self):
        """
        Removes the key with the smallest priority and returns a tuple containing the key and its associated priority
        """
        
        # Swap the last node to the front
        self._swap(0, len(self._heap) - 1)
        
        # Remove the smallest from the list
        (key, priority) = self._heap.pop()
        del self._keyindex[key]
        
        # Fix the heap
        self._heapify_down(0)
        
        return (key, priority)
        
    def update(self, key, priority):
        """
        update(key, priority)
        If priority is lower than the associated priority of key, then change it to the new priority. If not, does nothing.

        If key is not in the priority queue, add it.
        
        Return True if a change was made, else False.
        """
        
        if key in self._keyindex:
            # Find key index in heap
            i = self._keyindex[key]
            
            # Make sure this lowers its priority
            if priority > self._priority(i):
                return False
            
            # Fix the heap
            self._heap[i] = (key, priority)
            self._heapify_up(i)
            return True
        else:
            self._heap.append((key, priority))
            self._keyindex[key] = len(self._heap) - 1
            self._heapify_up(len(self._heap) - 1)
            return True
        
    def is_empty(self):
        """
        Returns True if the queue is empty empty, else False.
        """
        return len(self) == 0
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()
