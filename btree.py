import typing 

class Node: 

    def __init__(self,t):
        #NOTE: consider whether or not the bounds (t) change the node representation
        self.subtrees = []
        self.elements = []
        self.parent = None # initalise to a root node 
        self.t = t 

    def __str__(self): 
        return f"{self.elements}" 

    def __repr__(self):
        return f"{self.elements}" 

    def __lt__(self, other: 'Node'): 
        return self.elements < other.elements

    def binary_search(self, target: int) -> int: # DONE 

        lo, hi = 0, len(self.elements) - 1 

        while lo <= hi: 

            mid = (lo + hi) // 2 

            if self.elements[mid] == target: 
                return mid # we have found the element  
            elif self.elements[mid] < target: 
                lo = mid + 1 
            else:
                hi = mid - 1 

        return lo 
    
    def elementsFull(self) -> bool: 
        return len(self.elements) >= (2*self.t)-1

    def isLeaf(self): 
        return len(self.subtrees) == 0 

    def getMedian(self) -> int: 
        n = len(self.elements) - 1
        return n//2, self.elements[n//2]

    def isRoot(self) -> bool: 
        return self.parent == None 

class Btree: 

    def __init__(self, t): 
        self.root = Node(t)
        self.t = t 

    def insert(self, num: int) -> None:
        '''
        Case1: Just inserting into the leaf node (can be root)
        Case2: Inserting into root -> breakage 
        Case3: Inserting into leaf node -> breakage 
        '''

        if self.root.elementsFull():
            self.split(self.root)

        curr = self.root 

        # move through the b tree and determine if we need to split (pushing up split elements)
        while not curr.isLeaf(): 
            
            # traversing deeper 
            insertPos = curr.binary_search(num)
            
            # we have already inserted it so in that case we do not need to insert again 
            if (insertPos<len(curr.elements) and 
                curr.elements[insertPos] == num): 
                return 

            valid_child = curr.subtrees[insertPos]

            if valid_child.elementsFull():
                curr = self.split(valid_child)
                insertPos = curr.binary_search(num)
                valid_child = curr.subtrees[insertPos]

            curr = valid_child

        # inserting the node at the valid position 
        insertPos = curr.binary_search(num)
        curr.elements.insert(insertPos, num)
    
    def split(self, curr: 'Node') -> 'Node': 
        '''
        Recursively split the nodes
        '''

        while curr.elementsFull(): 

            if curr.isRoot(): 
                curr = self.splitting_root(curr)
                break 

            parent = self.splitting_internal_node(curr)
            curr = parent

        return curr
    
    def splitting_root(self, root: 'Node') -> None: 

        # create 2 child nodes
        left, right = Node(self.t), Node(self.t)
        # get the median and the median index because we need to slice around median 
        medianIndex, median = root.getMedian()

        if not root.isLeaf(): 
            left.subtrees = root.subtrees[:medianIndex+1]
            right.subtrees = root.subtrees[medianIndex:]

            for child in left.subtrees:
                child.parent = left
            for child in right.subtrees:
                child.parent = right
        
        # slice the elements based on the median 
        left.elements, right.elements = root.elements[:medianIndex], root.elements[medianIndex+1:]
        # make the parents of the left and right the root
        left.parent, right.parent = root, root 

        # the median is the element list 
        root.elements = [median]
        # the left and right are now the sub trees 
        root.subtrees = [left, right]

        return root 

    def splitting_internal_node(self, curr: 'Node') -> 'Node': 
        
        parent = curr.parent 
        medianIndex, median = curr.getMedian()
        insertPos = parent.binary_search(median)

        # add median into the parent 
        parent.elements.insert(insertPos, median)

        left, right = Node(self.t), Node(self.t)
        left.elements, right.elements = curr.elements[:medianIndex], curr.elements[medianIndex+1:]

        # insert child nodes on the left and right of the parent 
        #NOTE: make sure they are in order 
        parent.subtrees.insert(insertPos+1, right)
        parent.subtrees.insert(insertPos, left)
        parent.subtrees.remove(curr)

        left.parent, right.parent = parent, parent 

        if not curr.isLeaf(): 
            left.subtrees = curr.subtrees[:medianIndex+1]
            right.subtrees = curr.subtrees[medianIndex+1]

            for child in left.subtrees:
                child.parent = left
            for child in right.subtrees:
                child.parent = right

        return curr.parent  

if __name__ == "__main__": 

    b = Btree(2)
    insertions = [-1,0,1,2,3,4,5,6]

    for i in insertions: 
        b.insert(i)

    print(b.root)
    print(b.root.subtrees)



