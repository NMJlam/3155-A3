from node import Node 
from typing import *
from queue import Queue 
from collections import defaultdict 

class BTree:

    def __init__(self, t:int): 

        self.root = Node([],[])
        self.upper = 2*t - 1
        self.lower = t-1 

    def insert(self, num:int) -> None: 

        if self.root.num_keys() >= self.upper: 
            self.root = self.root.split_new_root()

        curr = self.root 

        while not curr.is_leaf(): 

            idx = curr.search(num)
            child = curr.children[idx]

            if child.num_keys() >= self.upper: 

                curr.split_child_at(idx)

                if curr.keys[idx] < num:
                    idx += 1

            curr = curr.children[idx]

        curr.insert(num)

    def insert_rec(self, num:int, curr: 'Node') -> None: 

        if self.root.num_keys() == self.upper: 
            self.root = self.root.split_new_root()

        if curr.is_leaf():
            curr.insert(num)
            return 
        
        idx = curr.search(num)
        child = curr.children[idx]

        if child.num_keys() >= self.upper: 
            curr.split_child_at(idx)

            if curr.keys[idx] < num:
                idx += 1 

        self.insert_rec(num, curr.children[idx])

    def search(self, num:int) -> int: 

        curr = self.root 

        while not curr.contains(num) and not curr.is_leaf(): 
            idx = curr.search(num)
            curr = curr.children[idx]

        return (curr, idx) if curr.contains(num) else None

    def delete(self, num:int) -> int: 
        pass 


    def breadth_first_search(self) -> Dict[int, List[int]]: 

        if not self.root: 
            return []

        layers = defaultdict(list)
        level = 0 
        queue = Queue() 
        queue.put([level, self.root])

        while not queue.empty(): 

            level, node = queue.get() 

            for child in node.children:
                queue.put([level+1, child])

            layers[level].append(node.keys)

        return layers 

    
    def __str__(self): 
        layers = self.breadth_first_search()
        sorted_key_values = sorted(layers.items(), key=lambda x: x[0])
        output = ""
        for level, keys in sorted_key_values:
            output += f"Level {level}: {keys}\n"
        return output

if __name__ == '__main__': 
    b = BTree(2)
    insertions = [1,2,3,4,5,6,9,10,-1,0,-2,-3,-4,-5]

    for i in insertions: 
        b.insert_rec(i, b.root)

    print(b.search(100))


    



