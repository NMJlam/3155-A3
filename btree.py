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

    def hasSpace(self) -> bool: 
        return len(self.elements) < (2*self.t)-1
    
    def isLeaf(self): 
        return len(self.subtrees) == 0 

    def getMedian(self) -> int: 
        n = len(self.elements) - 1
        return n//2, self.elements[n//2]


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

        # traverse the tree and then find a place to break, return insertion point 
        curr = self.root 
        insertPos = 0 

        if curr.elementsFull(): 
            curr = self.split_root(curr)

        while not curr.isLeaf(): 

            insertPos = curr.binary_search(num)

            if (insertPos<len(curr.elements) and 
                self.elements[insertionPosition] == num): 
                return 

            curr = curr.subtrees[insertPos]
        
        insertPos = curr.binary_search(num)
        curr.elements.insert(insertPos, num)
    
    def split_root(self, curr: 'Node') -> 'Node': 
        '''
        Return the top node that we split 
        '''
        left, right = Node(self.t), Node(self.t)
        
        medianIndex, median = curr.getMedian()
        left.elements, right.elements = curr.elements[:medianIndex], curr.elements[medianIndex+1:]
        #TODO: children not done yet WIP 

        curr.elements = [median]
        
        curr.subtrees.append(left)
        curr.subtrees.append(right)

        return curr 

if __name__ == "__main__": 

    b = Btree(2)
    insertion = [1,2,3,4]

    for i in insertion: 
        b.insert(i)

    print(b.root)

    for c in b.root.subtrees: 
        print("hit")
        print(c)





