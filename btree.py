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
        n = len(self.elements) 
        return self.elements[n//2]


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
        curr = self.root

        # inserts at that found leaf node if it has space then we dont need to balance 
        if curr.hasSpace(): 
            insertionPos = curr.binary_search(num)
            curr.elements.insert(insertionPos, num)
            return 
        
        # once inserted we must balance it
        if not curr.hasSpace(): 

            median = curr.getMedian() 

            left, right = Node(self.t), Node(self.t)
            
            # slice the left and right side 
            leftElem, rightElem = curr.elements[:median-1], curr.elements[median:]
            left.elements, right.elements = leftElem, rightElem
            left.parent, right.parent = curr, curr

            curr.subtrees.append(left)
            curr.subtrees.append(right)
            curr.elements = [median]
        
        insertionNode = self.root 
        while not insertionNode.isLeaf():  

            insertionPos = insertionNode.binary_search(num)

            # num where are trying to insert exists -> just ignore
            if insertionPos < len(insertionNode.elements) and insertionNode.elements[insertionPos] == num: 
                return 

            insertionNode = insertionNode.subtrees[insertionPos]

        i = insertionNode.binary_search(num)
        insertionNode.elements.insert(i,num)


if __name__ == "__main__": 

    b = Btree(2)
    insertion = [1,2,3,4]

    for i in insertion: 
        b.insert(i)

    print(b.root)

    for child in b.root.subtrees:
        print(child)





