from node import Node 
from queue import Queue 
from collections import defaultdict 
from typing import Tuple, List, Dict

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

    def search(self, num:int) -> Tuple['Node', int] | None: 

        curr = self.root 
        idx = 0 

        while not curr.contains(num) and not curr.is_leaf(): 
            idx = curr.search(num)
            curr = curr.children[idx]

        return (curr, idx) if curr.contains(num) else None 

    def delete(self, num:int) -> None:  
        # NOTE: Case 1 traverse down to a leaf and delete 

        curr = self.root 

        while not curr.is_leaf(): 

            idx = curr.search(num)

            # NOTE: here we find out if num in internal nodes
            if curr.contains(num): 

                left, right = curr.children[idx:idx+2]

                if left.num_keys() > self.lower:  
                    #NOTE: find predecessor 
                    pred = curr.predecessor(num) 
                    if pred: 
                        curr.keys[idx] = pred
                        num = pred

                elif right.num_keys() > self.lower: 
                    # NOTE: find successor
                    succ = curr.successor(num)
                    if succ: 
                        curr.keys[idx] = succ  
                        num = succ 
                        idx += 1 
                else: 
                    #NOTE: merge the LHS and the RHS 
                    curr.merge(idx)

            curr = curr.children[idx] 

        curr.delete(num)

    def rotate(self, idx: int, curr: 'Node') -> None: 
        pass 

    def breadth_first_search(self) -> Dict[int, List[int]]: 

        if not self.root: 
            return {} 

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
    insertions = [42, 7, 93, 58, 21, 84, 36, 19, 67, 10] 


    for i in insertions: 
        b.insert_rec(i, b.root)

    print(b)
    b.delete(42)
    b.delete(93)
    b.insert(22)
    print(b)
    b.delete(67)
    print(b)
    b.delete(36)
    print(b)

